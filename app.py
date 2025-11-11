from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados Render PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://crm_herlon_db_user:aOKoqHVB8Q8P4h9hWHjE19bezKSDo9Ke@dpg-d49ljo3ipnbc73e3orh0-a/crm_herlon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

# Cria as tabelas no banco
with app.app_context():
    db.create_all()

# Rota principal
@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

# Rota para adicionar cliente
@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(novo_cliente)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
