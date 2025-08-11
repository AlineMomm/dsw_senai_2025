from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = 'Aqui_deve_ter_uma_chave_secreta'  # EM PRODUÇÃO NÃO FAZER ISSO
                                                    # import secrets; print(secrets.token_hex(16))
                                                    

# /login = GET

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] == 'admin' and request.form['senha'] == 'senha123':
            flash('Login realizado com sucesso', 'sucesso')  # mensagem, categoria (string)
            return redirect(url_for('index'))   # redireciona para o index
        else:
            flash('Usuário ou senha incorretos!', 'erro')
            return redirect(url_for('login'))   # redireciona para ele mesmo
    return render_template('login.html')

@app.route('/logout')
def logout():
    flash('Sessão encerrada com sucesso','info')
    return redirect(url_for('index'))
                                                    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
