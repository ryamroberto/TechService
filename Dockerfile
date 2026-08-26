# =============================================================================
# TechService API — Dockerfile
# Story 4.2: Execução local com Docker
#
# Imagem simples para execução local da TechService API em container.
# Ambiente: Python 3.13 (slim), SQLite, servidor de desenvolvimento Django.
# Nenhuma credencial de produção embutida — SECRET_KEY fornecida em runtime.
# =============================================================================

FROM python:3.13-slim

# Evita criação de arquivos .pyc e garante saída de logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalação de dependências a partir de requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Cópia do código-fonte da aplicação
COPY . /app/

# Porta padrão de desenvolvimento exposta
EXPOSE 8000

# Inicialização do servidor de desenvolvimento Django em 0.0.0.0:8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
