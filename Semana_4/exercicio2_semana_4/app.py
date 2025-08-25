import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import DateField
from datetime import date


# Configuração da Aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Definição do Formulário
class EventoForm(FlaskForm):
    nome_evento = StringField(
        'Nome do Evento', 
        validators=[DataRequired(message='Campo obrigatório')],
    )
    data_evento = DateField(
        'Data do Evento',
        validators=[DataRequired(message='Campo obrigatório')],
        format='%Y-%m-%d'  # formato padrão do input type="date"
    )
    organizador = StringField(
        'Organizador', 
        validators=[DataRequired(message='Campo obrigatório')],
    )

    tipo_evento = SelectField(
        'Tipo de Evento',
        choices=[
            ('Palestra', 'Palestra'),
            ('Workshop', 'Workshop'),
            ('Meetup', 'Meetup'),
            ('Outro', 'Outro')
        ],
        validators=[DataRequired(message='Selecione um tipo de evento')]
    )

    descricao = TextAreaField('Descrição (obrigatória apenas se for "Outro")')
    enviar = SubmitField('Enviar')
    
    
    # Validador: não permitir datas passadas
    def validate_data_evento(self, field):
        if field.data and field.data < date.today():
            raise ValidationError("A data do evento não pode estar no passado.")

    # Validador condicional: descricao obrigatória se tipo_evento == "Outro"
    def validate_descricao(self, field):
        if self.tipo_evento.data == 'Outro' and (not field.data or not field.data.strip()):
            raise ValidationError("A descrição é obrigatória quando o tipo de evento é 'Outro'.")


# DEFINIÇÃO DE OBJETO MOCK PARA SIMULAÇÃO
class Evento:
    def __init__(self, nome_evento, data_evento, organizador, descricao=""):
        self.nome_evento = nome_evento
        self.data_evento = data_evento
        self.organizador = organizador
        self.descricao = descricao


# ROTAS DA APLICAÇÃO
@app.route('/')
def index():
    return render_template('index.html')


@app.route("/vazio", methods=['GET', 'POST'])
def formulario_vazio():
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        return render_template('sucesso.html', nome_usuario=nome_evento)
    
    return render_template(
        'formulario.html',
        form=form,
        title="1. Formulário Vazio"
    )


@app.route("/via-argumentos", methods=['GET', 'POST'])
def formulario_via_argumentos():
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        return render_template('sucesso.html', nome_usuario=nome_evento)
    
    elif not form.is_submitted():
        dados_iniciais = {
            'nome_evento': 'Samba',
            'data_evento': date.today(),
            'organizador': 'Alan',
            'descricao': 'Exemplo preenchido via argumentos.'
        }
        form = EventoForm(**dados_iniciais)
    
    return render_template(
        'formulario.html',
        form=form,
        title='2. Formulário preenchido com argumentos',
    )


@app.route("/via-objeto", methods=['GET', 'POST'])
def formulario_via_objetos():
    form = EventoForm()
    
    if form.validate_on_submit():
        nome_evento = form.nome_evento.data
        return render_template('sucesso.html', nome_usuario=nome_evento)
    
    elif not form.is_submitted():
        evento_mock = Evento(
            nome_evento="Rock in Rio",
            data_evento=date.today(),
            organizador="Alan",
            descricao="Exemplo preenchido via objeto."
        )
        form = EventoForm(obj=evento_mock)
    
    return render_template(
        'formulario.html',
        form=form,
        title='3. Formulário preenchido por objeto',
    )


# EXECUÇÃO DA APLICAÇÃO
if __name__ == '__main__':
    app.run(debug=True)
