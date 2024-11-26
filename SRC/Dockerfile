# Usar a imagem oficial do Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo requirements.txt para dentro do contêiner
COPY requirements.txt /app/

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos da aplicação para dentro do contêiner
COPY . /app/

# Expor a porta que o Flask estará escutando (padrão é 5000)
EXPOSE 5000

# Definir o comando para rodar a aplicação usando Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]
