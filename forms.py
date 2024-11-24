from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

# -------------------------- Classe para formulário de registro ---------------------------
class RegistrationForm(FlaskForm):
    """
    Formulário para registro de novos usuários.
    - Email: Campo obrigatório e deve ser um endereço válido.
    - Password: Deve ter no mínimo 6 caracteres.
    - Confirm Password: Deve coincidir com o campo de senha.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')  # Botão para submeter o formulário

# -------------------------- Classe para formulário de login ---------------------------
class LoginForm(FlaskForm):
    """
    Formulário para login de usuários.
    - Email: Campo obrigatório e deve ser um endereço válido.
    - Password: Campo obrigatório.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')  # Botão para submeter o formulário

# -------------------------- Classe para formulário de transações ---------------------------
class TransactionForm(FlaskForm):
    """
    Formulário para adicionar ou editar transações financeiras.
    - User ID: Seleciona o ID do usuário associado à transação.
    - Amount: Valor da transação (campo obrigatório e deve ser um número válido).
    - Date: Data e hora da transação (opcional, padrão é o momento atual).
    - Category ID: Seleciona a categoria associada à transação.
    """
    user_id = SelectField('User ', coerce=int, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    date = DateTimeField('Date', format='%Y-%m-%d %H:%M:%S', default=datetime.utcnow, validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Transaction')  # Botão para submeter o formulário

# -------------------------- Classe para formulário de categorias ---------------------------
class CategoryForm(FlaskForm):
    """
    Formulário para adicionar ou editar categorias.
    - Name: Nome da categoria (campo obrigatório e com limite máximo de 50 caracteres).
    """
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Category')  # Botão para submeter o formulário
