import decimal

from flask import render_template, url_for, flash, redirect
from dietAnalysys import app, db, bcrypt
from dietAnalysys.forms import RegistrationForm, LoginForm, PorcjaForm, PorcjaDeleteForm
from dietAnalysys.models import AppUser, Porcja, Zalecana_dzienna_konsumpcja, Produkty_spozywcze
from flask_login import login_user, current_user, logout_user


@app.route("/", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        form = PorcjaForm()
        form_delete = PorcjaDeleteForm()
        if form.validate_on_submit():
            porcja = Porcja(nazwa_produktu_spozywczego=form.nazwa_produktu_spozywczego.data.nazwa, masa=form.mass.data, id_uzytkownika=current_user.id)
            db.session.add(porcja)
            nazwa = porcja.nazwa_produktu_spozywczego
            produkty = Produkty_spozywcze.query.filter_by(panstwo=current_user.panstwo, nazwa=nazwa)
            for produkt in produkty:
                skladnik = produkt.skladnik_odzywczy
                if skladnik == 'Ca':
                    current_user.ca += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Cu':
                    current_user.cu += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Fe':
                    current_user.fe += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Mg':
                    current_user.mg += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'P':
                    current_user.p += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'K':
                    current_user.k += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Se':
                    current_user.se += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Zn':
                    current_user.mg += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Vitamin_B12':
                    current_user.vitamin_b12 += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Vitamin_B3':
                    current_user.vitamin_b3 += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Vitamin_B2':
                    current_user.vitamin_b2 += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Vitamin_B1':
                    current_user.vitamin_b1 += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Vitamin_B6':
                    current_user.vitamin_b6 += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Vitamin_E':
                    current_user.vitamin_e += produkt.mg100_g * float(porcja.masa) / 100
                elif skladnik == 'Vitamin_K':
                    current_user.vitamin_k += produkt.mg100_g * float(porcja.masa) / 100
            db.session.commit()
            flash('Your portion has been added!', 'success')
            return redirect(url_for('home'))
        if form_delete.validate_on_submit():
            Porcja.query.filter_by(id_uzytkownika=current_user.id).delete()
            current_user.ca = 0
            current_user.cu = 0
            current_user.fe = 0
            current_user.mg = 0
            current_user.p = 0
            current_user.k = 0
            current_user.se = 0
            current_user.zn = 0
            current_user.vitamin_b12 = 0
            current_user.vitamin_b3 = 0
            current_user.vitamin_b2 = 0
            current_user.vitamin_b1 = 0
            current_user.vitamin_b6 = 0
            current_user.vitamin_e = 0
            current_user.vitamin_k = 0
            db.session.commit()
            flash('Your portions have been deleted!', 'success')
            return redirect(url_for('home'))
        porcje = Porcja.query.filter_by(id_uzytkownika=current_user.id)
        user_rdi = Zalecana_dzienna_konsumpcja.query.filter_by(wiek=current_user.wiek, plec=current_user.plec).one()
        score = round((min(current_user.ca / user_rdi.ca, 1) + min(current_user.cu / user_rdi.cu, 1) +
                      min(current_user.fe / user_rdi.fe, 1) + min(current_user.mg / user_rdi.mg, 1) +
                      min(current_user.p / user_rdi.p, 1) + min(current_user.k / user_rdi.k, 1) +
                      min(current_user.se / user_rdi.se, 1) + min(current_user.zn / user_rdi.zn, 1) +
                      min(current_user.vitamin_b12 / user_rdi.vitamin_b12, 1) +
                      min(current_user.vitamin_b3 / user_rdi.vitamin_b3, 1) +
                      min(current_user.vitamin_b2 / user_rdi.vitamin_b2, 1) +
                      min(current_user.vitamin_b1 / user_rdi.vitamin_b1, 1) +
                      min(current_user.vitamin_b6 / user_rdi.vitamin_b6, 1) +
                      min(current_user.vitamin_e / user_rdi.vitamin_e, 1) +
                      min(current_user.vitamin_k / user_rdi.vitamin_k, 1)) / 16 * 10)
        return render_template('home_logged_in.html', title='Home', form=form, porcje=porcje, form_delete=form_delete, user_rdi=user_rdi, user=current_user, score=score)
    else:
        return render_template('home.html', title='Home')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = AppUser(email=form.email.data, haslo=hashed_password, wiek=form.age.data, plec=form.gender.data,
                       panstwo=form.country.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = AppUser.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.haslo, form.password.data):
            login_user(user, False)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
