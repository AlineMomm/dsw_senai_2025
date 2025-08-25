# app.py - Construtor de Receitas Online
# Demonstração de Rotas, Templates, Formulários e Validação

# Importa as classes e funções necessárias do Flask.
from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid # Para gerar IDs únicos para as receitas

# Cria uma instância da aplicação.
app = Flask(__name__)

# Configura uma chave secreta para usar com flash messages e sessões (MANDATÓRIO para usar `session`).
app.config['SECRET_KEY'] = 'chave-super-secreta-para-receitas-online'

# --- Armazenamento de Receitas (em memória) ---
# Lista global para armazenar as receitas cadastradas.
# Cada receita será um dicionário com id, nome, ingredientes e modo de preparo.
# ATENÇÃO: Esta lista é temporária e será reiniciada a cada vez que o servidor for reiniciado.
receitas_cadastradas = []

# ---- Rotas (URLs) da Aplicação ----

@app.route('/')
def index():
    """
    Renderiza a página inicial, exibindo todas as receitas cadastradas.
    Possui um botão para criar uma nova receita.
    """
    return render_template('index.html', receitas=receitas_cadastradas)

@app.route('/nova-receita', methods=['GET', 'POST'])
def nova_receita():
    """
    Exibe o formulário para criação de uma nova receita e processa o envio do mesmo.
    - GET: Mostra o formulário vazio.
    - POST: Captura, valida os dados e, se válidos, adiciona a receita e redireciona.
            Em caso de erro de validação, exibe mensagens flash e repopula o formulário.
    """
    if request.method == 'POST':
        # Captura os dados do formulário
        nome_receita = request.form.get('nome_receita', '').strip()
        ingredientes = request.form.get('ingredientes', '').strip()
        modo_preparo = request.form.get('modo_preparo', '').strip()

        # Validação dos campos
        if not nome_receita:
            flash('O nome da receita é obrigatório!', 'danger')
        if not ingredientes:
            flash('Os ingredientes são obrigatórios!', 'danger')
        if not modo_preparo:
            flash('O modo de preparo é obrigatório!', 'danger')

        # Se houver erros, redireciona de volta ao formulário, repopulando os campos
        if not nome_receita or not ingredientes or not modo_preparo:
            return render_template('receita.html',
                                   nome_receita=nome_receita,
                                   ingredientes=ingredientes,
                                   modo_preparo=modo_preparo)

        # Se os dados forem válidos, cria um ID único e adiciona a receita
        nova_receita_obj = {
            'id': str(uuid.uuid4()), # Gera um ID único para a receita
            'nome': nome_receita,
            'ingredientes': ingredientes,
            'modo_preparo': modo_preparo
        }
        receitas_cadastradas.append(nova_receita_obj)

        # Armazena o ID da receita recém-criada na sessão para exibição posterior
        session['receita_id_criada'] = nova_receita_obj['id']

        flash('Sua receita foi adicionada com sucesso!', 'success')
        return redirect(url_for('receita_criada'))

    # Se for uma requisição GET, renderiza o formulário vazio
    return render_template('receita.html')

@app.route('/receita-criada')
def receita_criada():
    """
    Exibe os detalhes da receita que acabou de ser criada.
    Recupera o ID da receita da sessão e busca a receita na lista global.
    """
    receita_id = session.pop('receita_id_criada', None) # Pega o ID e remove da sessão

    if not receita_id:
        flash('Nenhuma receita foi criada recentemente ou a sessão expirou. Por favor, crie uma nova receita.', 'info')
        return redirect(url_for('nova_receita'))

    # Busca a receita na lista global usando o ID
    receita_encontrada = next((r for r in receitas_cadastradas if r['id'] == receita_id), None)

    if not receita_encontrada:
        flash('Receita não encontrada.', 'danger')
        return redirect(url_for('nova_receita'))

    return render_template('receita_criada.html', receita=receita_encontrada)

# Rota para visualizar uma receita específica por ID
@app.route('/receita/<string:receita_id>')
def visualizar_receita(receita_id):
    """
    Permite visualizar uma receita específica a partir de seu ID.
    Útil para links diretos da página inicial.
    """
    receita_encontrada = next((r for r in receitas_cadastradas if r['id'] == receita_id), None)

    if not receita_encontrada:
        flash('Receita não encontrada.', 'danger')
        return redirect(url_for('index')) # Redireciona para a página inicial se não encontrar

    return render_template('receita_criada.html', receita=receita_encontrada)


# ---- Executa a aplicação ----
if __name__ == '__main__':
    # Roda a aplicação no modo de depuração.
    app.run(port=5001,debug=True)
