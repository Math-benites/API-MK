from flask import Flask, render_template, request, flash, redirect
import paramiko
from segredos import MIKROTIK_HOST, out_password, out_connect_to  # Importando as variáveis e função de config
import secrets
import string
import os


app = Flask(__name__)
app.secret_key = "Matheus_benites"  # Substitua por algo seguro


# Função para enviar comandos via SSH
def execute_ssh_command(host, username, password, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password, port=22)
        
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        
        if error:
            return f"Erro: {error}"
        return output.strip()
    except Exception as e:
        return f"Erro na conexão: {str(e)}"


# Rota para exibir o formulário
@app.route('/')
def index():
    return render_template('index.html', mikrotik_host=MIKROTIK_HOST)



# Função para gerar senha aleatória de 16 caracteres
def generate_password(length=16):
    """Gera uma senha aleatória de 'length' caracteres contendo letras maiúsculas, minúsculas e números."""
    alphabet = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    password = ''.join(secrets.choice(alphabet) for i in range(length))  # Gera a senha
    return password


@app.route('/send_command', methods=['POST'])
def send_command():
    host = MIKROTIK_HOST
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    routes = request.form['routes']  # Captura o valor de "routes" enviado no formulário
    
    # Gerar uma nova senha a cada envio de comando
    out_password = generate_password()  # Gera a senha aqui, cada vez que o formulário for enviado

    # Comando a ser enviado via SSH, agora com o valor de routes
    command = f"ppp secret add name={name} password={out_password} profile=CLIENTES routes={routes}"
    vpn_command = f"/interface l2tp-client add allow=chap,mschap1,mschap2 comment=vpn1 connect-to={out_connect_to} disabled=no name=LVPN1 password={out_password} user={name}"
    
    result = execute_ssh_command(host, username, password, command)
    result_vpn = execute_ssh_command(host, username, password, vpn_command)
    
    if "Erro" in result or "Exception" in result or "Erro" in result_vpn:
        flash(f"Falha ao enviar comando: {result} | {result_vpn}", "error")
        script = None
        command_status = "Falha ao enviar o comando."
    else:
        flash("Comando enviado com sucesso!", "success")
        script = generate_script(name)  # Gera o script com o nome do cliente
        command_status = f"Comando enviado para {host} com sucesso!"

    return render_template(
        'index.html',
        mikrotik_host=host,
        script=script,
        command_status=command_status
    )


# Função para gerar o script com base no nome do cliente
def generate_script(uservpn):
    try:
        # Carrega o template do arquivo
        with open('script_template.txt', 'r') as file:
            template = file.read()
        # Substitui o placeholder pelo nome do cliente e outras variáveis
        return template.replace("{uservpn}", uservpn).replace("{out_password}", out_password).replace("{out_connect_to}", out_connect_to)
    except FileNotFoundError:
        return "Erro: Arquivo de template não encontrado."

@app.route('/load_pre_config', methods=['GET'])
def load_pre_config():
    # Lê o conteúdo do arquivo pre_config_script.txt
    try:
        with open('pre_config_script.txt', 'r', encoding='utf-8') as file:
            script_content = file.read()
        return script_content
    except FileNotFoundError:
        return "Erro: Arquivo de configuração pré-configurado não encontrado."    


if __name__ == '__main__':
    app.run(debug=True)
