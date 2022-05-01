from dietAnalysys import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))


class AppUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    haslo = db.Column(db.String(60), nullable=False)
    wiek = db.Column(db.Integer, nullable=False)
    plec = db.Column(db.String(10), nullable=False)
    panstwo = db.Column(db.String(50), nullable=False)
    ca = db.Column(db.Float, nullable=False, default=0)
    cu = db.Column(db.Float, nullable=False, default=0)
    fe = db.Column(db.Float, nullable=False, default=0)
    mg = db.Column(db.Float, nullable=False, default=0)
    p = db.Column(db.Float, nullable=False, default=0)
    k = db.Column(db.Float, nullable=False, default=0)
    se = db.Column(db.Float, nullable=False, default=0)
    zn = db.Column(db.Float, nullable=False, default=0)
    vitamin_b12 = db.Column(db.Float, nullable=False, default=0)
    vitamin_b3 = db.Column(db.Float, nullable=False, default=0)
    vitamin_b2 = db.Column(db.Float, nullable=False, default=0)
    vitamin_b1 = db.Column(db.Float, nullable=False, default=0)
    vitamin_b6 = db.Column(db.Float, nullable=False, default=0)
    vitamin_e = db.Column(db.Float, nullable=False, default=0)
    vitamin_k = db.Column(db.Float, nullable=False, default=0)
    porcje = db.relationship('Porcja', backref='jedzacy', lazy=True)

    def __repr__(self):
        return f"AppUser('{self.email}')"


class Porcja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    masa = db.Column(db.Float, nullable=False)
    nazwa_produktu_spozywczego = db.Column(db.String(300), nullable=False)
    id_uzytkownika = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)

    def __repr__(self):
        return f"{self.nazwa_produktu_spozywczego} {self.masa} g"

class Produkty_spozywcze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    panstwo = db.Column(db.String(50), nullable=False)
    nazwa = db.Column(db.String(300), nullable=False)
    skladnik_odzywczy = db.Column(db.String(100), nullable=False)
    jednostka = db.Column(db.String(100), nullable=False)
    poziom = db.Column(db.Float, nullable=False)
    mnoznik = db.Column(db.Float, nullable=False)
    mg100_g = db.Column(db.Float, nullable=False)


class Zalecana_dzienna_konsumpcja(db.Model):
    wiek = db.Column(db.Integer, nullable=False)
    plec = db.Column(db.String(10), nullable=False)
    ca = db.Column(db.Float, nullable=False)
    cu = db.Column(db.Float, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    fe = db.Column(db.Float, nullable=False)
    mg = db.Column(db.Float, nullable=False)
    p = db.Column(db.Float, nullable=False)
    k = db.Column(db.Float, nullable=False)
    se = db.Column(db.Float, nullable=False)
    zn = db.Column(db.Float, nullable=False)
    vitamin_b12 = db.Column(db.Float, nullable=False)
    vitamin_b3 = db.Column(db.Float, nullable=False)
    vitamin_b2 = db.Column(db.Float, nullable=False)
    vitamin_b1 = db.Column(db.Float, nullable=False)
    vitamin_b6 = db.Column(db.Float, nullable=False)
    vitamin_e = db.Column(db.Float, nullable=False)
    vitamin_k = db.Column(db.Float, nullable=False)
