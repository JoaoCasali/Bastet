from werkzeug.security import generate_password_hash, check_password_hash

# Função para criar um hash de uma senha
def criar_hash_senha(senha):
    return generate_password_hash(senha)

# Exemplo de uso
senha = "senha123"  # A senha que você deseja hashear
hash_senha = criar_hash_senha(senha)

print(f"Senha original: {senha}")
print(f"Hash da senha: {hash_senha}")

# Para verificar o hash
senha_inserida = "senha123"  # Senha que o usuário tenta inserir
if check_password_hash(hash_senha, senha_inserida):
    print("Senha correta!")
else:
    print("Senha incorreta!")