from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dietAnalysys.models import AppUser, Produkty_spozywcze
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_login import current_user


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Gender', choices=['M', 'F'])
    age = IntegerField('Age', validators=[DataRequired()])
    country = SelectField('Country',
                          choices=['Finland', 'Sweden', 'Italy', 'Germany', 'France', 'United Kingdom', 'Netherlands'])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):

        user = AppUser.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is already registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


def produkt_query():
    return Produkty_spozywcze.query.filter_by(panstwo=current_user.panstwo)


class PorcjaForm(FlaskForm):
    nazwa_produktu_spozywczego = QuerySelectField('name of food product', query_factory=produkt_query, allow_blank=False, validators=[DataRequired()], get_label='nazwa')
    mass = DecimalField('mass (in grams)', places=2, validators=[DataRequired()])
    submit = SubmitField('add portion')


class PorcjaDeleteForm(FlaskForm):
    submit = SubmitField('delete all portions')