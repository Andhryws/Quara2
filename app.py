from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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

# Página inicial
@app.route("/")
def index():
    usuarios = Usuario.query.all()
    return render_template("index.html", usuarios=usuarios)

# Página de cadastro
@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

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
@app.route("/produto")
def produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template("produto.html", usuario_nome=session.get('usuario_nome'))

# Página de busca
@app.route("/procurar")
def procurar():
    return render_template("procurar.html")

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5153)
