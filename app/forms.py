from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Service

class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=120)])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=1, max=20)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=1, max=128)])
    confirm_senha = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha')])
    agree_terms = BooleanField('Eu concordo com os', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_agree_terms(form, field):
        if not field.data:
            raise ValidationError('Você deve concordar com os termos e serviços para se cadastrar.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=120)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=1, max=128)])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Login')

class AppointmentForm(FlaskForm):
    servico = SelectField('Serviço', validators=[DataRequired()])
    data = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    hora = SelectField('Hora', validators=[DataRequired()])
    submit = SubmitField('Agendar')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.servico.choices = [(s.id, f"{s.nome} - R$ {s.preco}") for s in Service.query.all()]
        self.hora.choices = []
