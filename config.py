import secrets
import string

# Função para gerar senha aleatória de 16 caracteres
def generate_password(length=16):
    """Gera uma senha aleatória de 'length' caracteres contendo letras maiúsculas, minúsculas e números."""
    alphabet = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    password = ''.join(secrets.choice(alphabet) for i in range(length))  # Gera a senha
    return password

# Endereço IP do MikroTik
MIKROTIK_HOST = "192.168.1.16"  

# Gerar uma senha de 16 caracteres
out_password = generate_password()

# Defina o IP de conexão para a VPN
out_connect_to = "fln.ti.kiper.tec.br"
