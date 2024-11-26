from flask import Flask, render_template, request, flash, redirect
import paramiko
from config import MIKROTIK_HOST


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


# Rota para enviar o comando
@app.route('/send_command', methods=['POST'])
def send_command():
    host = request.form['host']
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    
    # Comando a ser enviado via SSH
    command = f"/ppp/secret/add name={name} password=Senh@PF_VPN#porter profile=CLIENTES"
    result = execute_ssh_command(host, username, password, command)
    
    if "Erro" in result or "Exception" in result:
        flash(f"Falha ao enviar comando: {result}", "error")
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



def generate_script(uservpn):
    try:
        # Carrega o template do arquivo
        with open('script_template.txt', 'r') as file:
            template = file.read()
        # Substitui o placeholder pelo nome do cliente
        return template.replace("{uservpn}", uservpn)
    except FileNotFoundError:
        return "Erro: Arquivo de template não encontrado."


if __name__ == '__main__':
    app.run(debug=True)
