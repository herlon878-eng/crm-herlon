from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configurações principais
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'segredo-herlon'

db = SQLAlchemy(app)

# Modelo de Lead
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(50), nullable=True)

# Modelo de Admin
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# Página inicial (leads)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form.get('nome', '')
        email = request.form.get('email', '')
        telefone = request.form.get('telefone', '')

        # Agora todos os campos são opcionais
        novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
        db.session.add(novo_cliente)
        db.session.commit()

        flash('✅ Lead cadastrado com sucesso!')
        return redirect(url_for('index'))

    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

# Excluir lead
@app.route('/excluir/<int:id>')
def excluir(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        flash('❌ Lead excluído com sucesso!')
    return redirect(url_for('index'))

# Criar admin
@app.route('/criar_admin', methods=['GET', 'POST'])
def criar_admin():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario and senha:
            senha_hash = generate_password_hash(senha)
            novo_admin = Admin(usuario=usuario, senha=senha_hash)
            db.session.add(novo_admin)
            db.session.commit()
            return "✅ Admin criado com sucesso!"
        else:
            return "❌ Preencha todos os campos!"
    return render_template('criar_admin.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        admin = Admin.query.filter_by(usuario=usuario).first()
        if admin and check_password_hash(admin.senha, senha):
            return redirect(url_for('index'))
        else:
            return "❌ Usuário ou senha incorretos."
    return render_template('login.html')

# Erro 404 redireciona para index
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
