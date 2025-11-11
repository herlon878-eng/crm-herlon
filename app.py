from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_super_secreta'

db = SQLAlchemy(app)

# ========================
# MODELOS
# ========================
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

# ========================
# ROTAS
# ========================

@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    novo = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
    return redirect(url_for('index'))

# ========================
# LOGIN / ADMIN
# ========================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario'] = usuario.username
            return redirect(url_for('index'))
        else:
            return "Usuário ou senha incorretos"

    return '''
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Usuário"><br>
            <input name="senha" type="password" placeholder="Senha"><br>
            <button type="submit">Entrar</button>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/criar_admin')
def criar_admin():
    if not Usuario.query.filter_by(username='admin').first():
        senha_hash = generate_password_hash('1234')
        admin = Usuario(username='admin', senha=senha_hash)
        db.session.add(admin)
        db.session.commit()
        return "Usuário admin criado com sucesso! (usuário: admin, senha: 1234)"
    else:
        return "Usuário admin já existe."

# ========================
# INICIALIZAÇÃO
# ========================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=10000)
