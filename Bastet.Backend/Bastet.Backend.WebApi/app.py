import jwt
import datetime
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash

# Chave secreta para assinar o JWT
SECRET_KEY = '364123415312'

usuarios = {
    "usuario_exemplo": {
        "password": "scrypt:32768:8:1$nxWxGoOtASjPZOm9$296e0d331ef5a9bc4351858be089358d6435c614ec0c813f05fdadceced73ed6fd3707ba6a298fa882f6f9293b60f3d74ab1ff440a577987293dfd4a23070845"  # hash de 'senha123'
    }
}

app = Flask(__name__)

# Definindo uma lista de rotas que não precisam de autenticação
no_auth_routes = []
def no_auth(f):
    no_auth_routes.append(f.__name__)
    return f

# Middleware para verificar o token em todas as requisições
@app.before_request
def check_token():
    # Se a rota estiver na lista de exclusão, não verificamos o token
    if request.endpoint in no_auth_routes:
        return

    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token inválido!'}), 403

    try:
        # Validando o token JWT
        jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido!'}), 403

# Rota base - pública
@no_auth
@app.route('/')
def hello_world():
    return "Olá, mundo!"

@no_auth
@app.route('/Token', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Verificando se o usuário existe e se a senha está correta
    if username not in usuarios or not check_password_hash(usuarios[username]['password'], password):
        return jsonify({"message": "Usuário ou senha inválidos"}), 401

    # Gerando o token JWT
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expira em 30 minutos
    }, SECRET_KEY)

    return jsonify({"token": token})

@app.route('/protegido', methods=['GET'])
def rota_protegida():
    return jsonify({"message": "Você acessou uma rota protegida com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)