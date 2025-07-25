from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
# Adicione após criar a app Flask
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')  # Pasta para uploads dentro de static

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = '9f1c2d4a8eab3e7b6f9c1d2e3a4b5c6d'  # ESSENCIAL para sessões
db = SQLAlchemy(app)

# Configurações de upload (adicione no início do arquivo)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Adicione este campo

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
    # Obter usuários (mantenha o que já tinha)
    usuarios = Usuario.query.all()
    
    # Adicionar os produtos recentes
    produtos_recentes = Produto.query.order_by(Produto.id.desc()).limit(4).all()
    
    return render_template(
        "index.html",
        usuarios=usuarios,
        produtos_recentes=produtos_recentes  # Passando para o template
    )

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

# Rota para adicionar produto
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
    usuario = None
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
    return render_template('produto.html', produto=produto, usuario=usuario)

# Página de busca
@app.route('/procurar')
def procurar():
    # Produtos recentes (últimos 6 adicionados)
    produtos_recentes = Produto.query.order_by(Produto.id.desc()).limit(6).all()
    
    # Todas as categorias existentes (dinâmico)
    categorias = db.session.query(Produto.categoria.distinct()).all()
    categorias = [categoria[0] for categoria in categorias if categoria[0]]  # Extrai os valores
    
    produtos_por_categoria = {}
    for categoria in categorias:
        produtos = Produto.query.filter_by(categoria=categoria).all()
        if produtos:  # Só adiciona se tiver produtos
            produtos_por_categoria[categoria] = produtos
    
    return render_template(
        'procurar.html',
        produtos_recentes=produtos_recentes,
        produtos_por_categoria=produtos_por_categoria
    )

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

@app.route('/produto/<int:produto_id>/editar', methods=['GET', 'POST'])
def editar_produto(produto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    produto = Produto.query.get_or_404(produto_id)
    usuario = Usuario.query.get(session['usuario_id'])
    
    if produto.usuario_id != usuario.id and not usuario.is_admin:
        return "Acesso não autorizado", 403
    
    if request.method == 'POST':
        # Atualiza todos os campos diretamente do formulário
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.tamanho = request.form['tamanho']
        produto.tipo = request.form['tipo']
        produto.preco = float(request.form['preco'])
        produto.categoria = request.form['categoria']
        produto.Contato = request.form['contato']
        produto.imagem = request.form['imagem']  # Armazena apenas a URL
        
        db.session.commit()
        return redirect(url_for('detalhes_produto', produto_id=produto.id))
    
    return render_template('mod_produto.html', produto=produto)


# Adicione esta rota para excluir produtos
@app.route('/produto/<int:produto_id>/excluir', methods=['POST'])
def excluir_produto(produto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    produto = Produto.query.get_or_404(produto_id)
    usuario = Usuario.query.get(session['usuario_id'])
    
    # Verifica se é o dono ou admin
    if produto.usuario_id != usuario.id and not usuario.is_admin:
        return "Acesso não autorizado", 403
    
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('procurar'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5153)
