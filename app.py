from flask import Flask, request, jsonify, redirect, flash, render_template, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Chave secreta para sessões Flask, altere para uma chave segura em produção

# Caminhos para os arquivos CSV usados como "banco de dados"
CSV_USERS_FILE = 'data/users.csv'
CSV_TRANSACTIONS_FILE = 'data/transactions.csv'
CSV_CATEGORIES_FILE = 'data/categories.csv'


# -------------------------- Funções auxiliares para manipulação de arquivos CSV ---------------------------

# Lê os dados de um arquivo CSV e retorna uma lista de dicionários
def read_from_csv(file_path):
    if not os.path.isfile(file_path):  # Retorna lista vazia se o arquivo não existir
        return []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]  # Converte as linhas em uma lista de dicionários


# Escreve um novo registro em um arquivo CSV
def write_to_csv(file_path, data, fields):
    file_exists = os.path.isfile(file_path)  # Verifica se o arquivo já existe
    with open(file_path, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if not file_exists:
            writer.writeheader()  # Escreve o cabeçalho se o arquivo for novo
        writer.writerow(data)


# Remove uma entrada de um arquivo CSV com base em um identificador único (ID)
def delete_from_csv(file_path, identifier):
    rows = read_from_csv(file_path)
    updated_rows = [row for row in rows if row['id'] != str(identifier)]  # Filtra linhas pelo ID
    if updated_rows:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            writer.writerows(updated_rows)  # Escreve as linhas restantes


# Atualiza uma categoria existente no arquivo CSV com base no ID
def edit_category_in_csv(category_id, new_name):
    categories = read_from_csv(CSV_CATEGORIES_FILE)
    for category in categories:
        if str(category_id) == category['id']:  # Encontra a categoria pelo ID
            category['name'] = new_name  # Atualiza o nome
            break
    with open(CSV_CATEGORIES_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name'])
        writer.writeheader()
        writer.writerows(categories)


# -------------------------- Rotas para gerenciamento de categorias ---------------------------

# Exibe a lista de categorias e permite adicionar novas
@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    categories = read_from_csv(CSV_CATEGORIES_FILE)
    if request.method == 'POST':
        # Adiciona uma nova categoria a partir do formulário
        new_category = {'id': len(categories) + 1, 'name': request.form['name']}
        write_to_csv(CSV_CATEGORIES_FILE, new_category, ['id', 'name'])
        flash('Categoria adicionada com sucesso!', 'success')
        return redirect(url_for('categorias'))
    return render_template('categories.html', categorias=categories)


# Edita uma categoria existente pelo ID
@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    categories = read_from_csv(CSV_CATEGORIES_FILE)
    current_category = next((cat for cat in categories if int(cat['id']) == category_id), None)

    if not current_category:
        flash('Categoria não encontrada.', 'danger')
        return redirect(url_for('categorias'))

    if request.method == 'POST':
        # Atualiza o nome da categoria a partir do formulário
        new_name = request.form.get('name', '').strip()
        if new_name:
            edit_category_in_csv(category_id, new_name)
            flash('Categoria editada com sucesso!', 'success')
        else:
            flash('O nome da categoria não pode estar vazio.', 'danger')
        return redirect(url_for('categorias'))

    return render_template('edit_category.html', category=current_category)


# Remove uma categoria pelo ID
@app.route('/delete_category/<int:category_id>')
def delete_category(category_id):
    delete_from_csv(CSV_CATEGORIES_FILE, category_id)
    flash('Categoria excluída com sucesso!', 'success')
    return redirect(url_for('categorias'))


# -------------------------- Rotas para gerenciamento de transações ---------------------------

# Exibe a lista de transações e permite adicionar novas
@app.route('/transacoes', methods=['GET', 'POST'])
def transacoes():
    transacoes = read_from_csv(CSV_TRANSACTIONS_FILE)
    categories = read_from_csv(CSV_CATEGORIES_FILE)

    if request.method == 'POST':
        # Adiciona uma nova transação a partir do formulário
        nova_transacao = {
            'id': len(transacoes) + 1,
            'descricao': request.form['descricao'],
            'valor': request.form['valor'],
            'categoria': request.form['categoria']
        }
        write_to_csv(CSV_TRANSACTIONS_FILE, nova_transacao, ['id', 'descricao', 'valor', 'categoria'])
        flash('Transação adicionada com sucesso!', 'success')
        return redirect(url_for('transacoes'))

    return render_template('transactions.html', transacoes=transacoes, categorias=categories)


# Remove uma transação pelo ID
@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    delete_from_csv(CSV_TRANSACTIONS_FILE, transaction_id)
    flash('Transação excluída com sucesso!', 'success')
    return redirect(url_for('transacoes'))


# -------------------------- Rotas para autenticação de usuários ---------------------------

# Tela de registro de novos usuários
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = read_from_csv(CSV_USERS_FILE)

        # Verifica se o e-mail já está registrado
        if any(user['email'] == email for user in users):
            flash('Esse email já está cadastrado. Tente outro.', 'danger')
            return redirect(url_for('register'))

        # Cria um novo usuário com senha criptografada
        new_user = {
            'id': len(users) + 1,
            'email': email,
            'password': generate_password_hash(password)
        }
        write_to_csv(CSV_USERS_FILE, new_user, ['id', 'email', 'password'])
        flash('Registro realizado com sucesso! Faça login agora.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


# Tela de login para usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = read_from_csv(CSV_USERS_FILE)
        user = next((u for u in users if u['email'] == email), None)
        if user and check_password_hash(user['password'], password):
            session['user'] = email
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('E-mail ou senha inválidos.', 'danger')
    return render_template('login.html')


# Realiza o logout do usuário
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('home'))


# -------------------------- Página inicial ---------------------------

# Página inicial com uma mensagem de boas-vindas
@app.route('/')
def home():
    user = session.get('user')  # Verifica se o usuário está logado
    return render_template('index.html', user=user)


# -------------------------- Inicialização da aplicação ---------------------------
if __name__ == '__main__':
    app.run(debug=True)  # Habilita o modo de depuração
