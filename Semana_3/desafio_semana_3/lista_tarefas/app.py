from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)

# Lista de tarefas
tarefas = []

# Página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tarefa = request.form.get('tarefa')
        data_limite = request.form.get("data_limite") 
        if tarefa and data_limite: 
            #Formatar data para formato brasileiro
            data_formatada = datetime.strptime(data_limite, "%Y-%m-%d").strftime("%d/%m/%Y")
            tarefas.append((tarefa, data_formatada))
        return redirect(url_for('sucesso', tarefa=tarefa, data_limite=data_formatada))
    return render_template('index.html', tarefas=tarefas) 

# Página desucesso
@app.route('/sucesso')
def sucesso():
    tarefa = request.args.get('tarefa')
    data_limite = request.args.get('data_limite')
    return render_template('sucesso.html', tarefa=tarefa, data_limite=data_limite)

# Limpar
@app.route("/limpar", methods=["POST"])
def limpar():
    tarefas.clear()
    return redirect(url_for("index"))

@app.route("/excluir/<int:indice>", methods=["POST"])
def excluir(indice):
    if 0 <= indice < len(tarefas):
        tarefas.pop(indice)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
