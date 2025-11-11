from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Banco de dados temporário (em memória)
clientes = []

@app.route('/')
def index():
    return render_template('index.html', clientes=clientes)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    clientes.append({'nome': nome, 'email': email, 'telefone': telefone})
    return redirect(url_for('index'))

@app.route('/excluir/<int:indice>')
def excluir(indice):
    clientes.pop(indice)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
