from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = 'chave-secreta-super-segura'  # troque depois

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------ MODELOS ------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

# ------------------ LOGIN ------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ------------------ ROTAS PRINCIPAIS ------------------

@app.route('/')
@login_required
def index():
    leads = Lead.query.all()
    return render_template('index.html', leads=leads)

@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    novo = Lead(nome=nome, email=email, telefone=telefone)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
@login_required
def excluir(id):
    lead = Lead.query.get(id)
    db.session.delete(lead)
    db.session.commit()
    return redirect(url_for('index'))

# ------------------ CRIAR USUÁRIO ADMIN ------------------

@app.route('/criar_admin')
def criar_admin():
    """Cria um usuário admin padrão (use apenas uma vez e depois apague)."""
    hashed_pw = bcrypt.generate_password_hash("admin123").decode('utf-8')
    novo_user = User(username="admin", password=hashed_pw)
    db.session.add(novo_user)
    db.session.commit()
    return "Usuário admin criado!"

if __name__ == '__main__':
    app.run(debug=True)
