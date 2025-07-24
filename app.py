from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = '9f1c2d4a8eab3e7b6f9c1d2e3a4b5c6d'  # ESSENCIAL para sessões
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    tamanho = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(255))  # Pode ser nome do arquivo ou URL
    categoria = db.Column(db.String(50), nullable=False)
    Contato = db.Column(db.String(50), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('produtos', lazy=True))

# Página inicial
@app.route("/")
def index():
    usuarios = Usuario.query.all()
    return render_template("index.html", usuarios=usuarios)

# Página de cadastro
@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

@app.route('/usuario')
def usuario_pg():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    id_usuario = session['usuario_id']
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return "Usuário não encontrado", 404

    return render_template('usuario.html', usuario=usuario)

@app.route('/add_produto')
def add_produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    id_usuario = session['usuario_id']
    usuario = Usuario.query.get(id_usuario)

    if not usuario:
        return "Usuário não encontrado", 404

    return render_template('add_produto.html', usuario=usuario)

# Página de login - GET exibe o formulário; POST processa login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            return redirect(url_for('procurar'))  # Redireciona para a página de busca
        else:
            flash('Email ou senha incorretos')
            return render_template("login.html")
    return render_template("login.html")

# Página de produtos - protegida, só acessa se estiver logado

@app.route('/produto/<int:produto_id>')
def detalhes_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template('produto.html', produto=produto)

# Página de busca
@app.route('/procurar')
def procurar():
    produtos = Produto.query.all()
    return render_template('procurar.html', produtos=produtos)

# Cadastro de usuário (POST)
@app.route("/create", methods=['POST'])
def create_usuario():
    nome = request.form['nome']
    existing_nome = Usuario.query.filter_by(nome=nome).first()
    if existing_nome:
        return "Usuário já cadastrado", 400
    cpf = request.form['cpf']
    existing_cpf = Usuario.query.filter_by(cpf=cpf).first()
    if existing_cpf:
        return "CPF já cadastrado", 400
    nascimento = request.form['aniversario']
    nascimento = datetime.strptime(nascimento, "%Y-%m-%d").date()
    email = request.form['email']
    existing_email = Usuario.query.filter_by(email=email).first()
    if existing_email:
        return "Email já cadastrado", 400
    senha = request.form['senha']
    confirm_senha = request.form['confirm_senha']
    if senha != confirm_senha:
        return "As senhas não coincidem", 400
    senha_hash = generate_password_hash(senha)
    novo_usuario = Usuario(nome=nome, cpf=cpf, nascimento=nascimento, email=email, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('login'))

# Deletar usuário
@app.route('/delete/<int:usuario_id>', methods=['POST'])
def delete_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect("/")

# Atualizar usuário
@app.route('/update/<int:usuario_id>', methods=['POST'])
def update_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario.nome = request.form['nome']
        usuario.cpf = request.form['cpf']
        usuario.nascimento = datetime.strptime(request.form['aniversario'], "%Y-%m-%d").date()
        usuario.email = request.form['email']
        usuario.senha = generate_password_hash(request.form['senha'])
        db.session.commit()
    return redirect("/")

# Logout - limpa sessão
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/produtos/create', methods=['POST'])
def create_produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    nome = request.form['nome']
    descricao = request.form['descricao']
    tamanho = request.form['tamanho']
    tipo = request.form['tipo']
    preco = float(request.form['preco'])
    imagem = request.form.get('imagem')  # Pode ser um campo opcional
    categoria = request.form['categoria']
    contato = request.form['contato']
    usuario_id = session['usuario_id']

    novo_produto = Produto(
        nome=nome,
        descricao=descricao,
        tamanho=tamanho,
        tipo=tipo,
        preco=preco,
        imagem=imagem,
        categoria=categoria,
        Contato=contato,
        usuario_id=usuario_id
    )
    db.session.add(novo_produto)
    db.session.commit()

    return redirect(url_for('procurar'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5153)
