from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'segredo-herlon'

# Conexão com o banco PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tabelas
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# 🔒 Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        user = Usuario.query.filter_by(username=username).first()

        if user and check_password_hash(user.senha, senha):
            session['user'] = user.username
            return redirect(url_for('index'))
        else:
            return "Usuário ou senha incorretos!"

    return '''
        <form method="POST">
            <h2>Login</h2>
            <input type="text" name="username" placeholder="Usuário" required><br>
            <input type="password" name="senha" placeholder="Senha" required><br>
            <button type="submit">Entrar</button>
        </form>
    '''

# 🔐 Criar admin manualmente (usar 1x)
@app.route('/criar_admin')
def criar_admin():
    if Usuario.query.filter_by(username='admin').first():
        return "Admin já existe."
    senha_hash = generate_password_hash("1234")
    novo = Usuario(username='admin', senha=senha_hash)
    db.session.add(novo)
    db.session.commit()
    return "Usuário admin criado com sucesso!"

# 🏠 Página principal
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'user' not in session:
        return redirect(url_for('login'))

    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']

    novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(novo_cliente)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
