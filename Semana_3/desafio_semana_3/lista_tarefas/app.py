from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de tarefas
tarefas = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tarefa = request.form.get('tarefa')
        data_limite = request.form.get("data_limite") 
        if tarefa and data_limite: 
            tarefas.append((tarefa, data_limite)) # tupla (0,1)
        return redirect(url_for('sucesso', tarefa=tarefa, data_limite=data_limite))
    return render_template('index.html', tarefas=tarefas) 

@app.route('/sucesso')
def sucesso():
    tarefa = request.args.get('tarefa')
    data_limite = request.args.get('data_limite')
    return render_template('sucesso.html', tarefa=tarefa, data_limite=data_limite)

if __name__ == '__main__':
    app.run(debug=True)
