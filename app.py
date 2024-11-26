from flask import Flask, render_template, request, flash, redirect
import paramiko

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Substitua por algo seguro

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
    return render_template('index.html')

# Rota para enviar o comando
@app.route('/send_command', methods=['POST'])
def send_command():
    host = request.form['host']
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    user_password = request.form['user_password']
    
    command = f"/ppp/secret/add name={name} password={user_password} profile=CLIENTES"
    result = execute_ssh_command(host, username, password, command)
    
    if "Erro" in result or "Exception" in result:
        flash(f"Falha ao enviar comando: {result}", "error")
    else:
        flash("Comando enviado com sucesso!", "success")
    
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
