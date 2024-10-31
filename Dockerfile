# Escolha a imagem base
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /piza

# Copie o arquivo de requisitos para o container
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o container
COPY . .

# Exponha a porta em que o Gunicorn irá rodar
EXPOSE 9999

# Comando para rodar a aplicação usando Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:9999 config.wsgi:application"]
