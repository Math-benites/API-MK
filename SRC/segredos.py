import configparser
import secrets
import string

# Função para gerar senha aleatória de 16 caracteres
def generate_password(length=16):
    """Gera uma senha aleatória de 'length' caracteres contendo letras maiúsculas, minúsculas e números."""
    alphabet = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    password = ''.join(secrets.choice(alphabet) for i in range(length))  # Gera a senha
    return password

# Carregar o arquivo de configuração
config = configparser.ConfigParser()
config.read('config.ini')

# Obter as variáveis do arquivo de configuração
MIKROTIK_HOST = config.get('settings', 'MIKROTIK_HOST')
out_connect_to = config.get('settings', 'out_connect_to')

# Gerar uma senha de 16 caracteres
out_password = generate_password()

print(f'MIKROTIK_HOST: {MIKROTIK_HOST}')
print(f'out_connect_to: {out_connect_to}')
print(f'out_password: {out_password}')
