from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'

# FORMULÁRIOS

class MeuFormulario(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    email = StringField('Seu Melhor E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),
        Email(message="Por favor, insira um e-mail válido.")
    ])
    submit = SubmitField('Enviar Cadastro')

class FormularioRegistro(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    email = StringField('E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),
        Email(message="Insira um e-mail válido.")
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message="A senha é obrigatória."),
        Length(min=8, message="A senha deve ter pelo menos 8 caracteres.")
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message="Confirme sua senha."),
        EqualTo('senha', message="As senhas devem ser iguais.")
    ])
    biografia = TextAreaField('Biografia (opcional)')
    aceitar_termos = BooleanField('Aceito os Termos de Serviço', validators=[
        DataRequired(message="Você deve aceitar os termos para continuar.")
    ])
    submit = SubmitField('Registrar')

# ROTAS
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MeuFormulario()
    if form.validate_on_submit():
        flash(f'Cadastro recebido com sucesso para {form.nome.data} ({form.email.data})!', 'success')
        return redirect(url_for('formulario'))
    return render_template('formulario.html', form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    if form.validate_on_submit():
        nome = form.nome.data
        bio = form.biografia.data.strip() if form.biografia.data else None
        if bio:
            flash(f'Bem-vindo, {nome}! Sua biografia: "{bio[:60]}..."', 'success')
        else:
            flash(f'Bem-vindo, {nome}! Registro realizado com sucesso.', 'success')
        return redirect(url_for('registro'))
    return render_template('registro.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
