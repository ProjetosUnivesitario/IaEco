# 🌱 IaEco Backend - Cálculo de Pegada de Carbono

![Status do Deploy](https://img.shields.io/badge/deploy-online-brightgreen)  
![Licença](https://img.shields.io/badge/license-MIT-blue.svg)

O **IaEco Backend** é uma API desenvolvida em **Django REST Framework** para gerenciar o cálculo e visualização da pegada de carbono, baseada nos escopos do **GHG Protocol** (Escopos 1, 2 e 3). Ele suporta autenticação JWT, upload e processamento assíncrono de documentos, e integração com um frontend React para uma experiência interativa e responsiva.

---

## ✅ Requisitos

- **Python** versão **3.8 ou superior**
- **PostgreSQL** versão **12 ou superior**
- **RabbitMQ** versão **3.8 ou superior**
- **Redis** versão **6 ou superior**
- **pip** e **venv** (geralmente incluídos com Python)
- **Git**

---

## 🚀 Instalação e Uso

### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/iaeco-backend.git
cd iaeco-backend
```

### 2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4. Configure o PostgreSQL:

Crie um banco de dados para o projeto:

### 5. Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto com base no exemplo fornecido:
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
PGDATABASE=iaeco_db
PGUSER=seu_usuario_postgres
PGPASSWORD=sua_senha_postgres
PGHOST=localhost
PGPORT=5432
EMAIL_HOST=smtp.seu_provedor.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email
EMAIL_HOST_PASSWORD=sua_senha_email
DEFAULT_FROM_EMAIL=seu_email@dominio.com
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//

### 6. Aplique as migrações do banco de dados:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crie um superusuário (opcional, para acesso ao admin):
```bash
python manage.py createsuperuser
```

### 8. Inicie o servidor Django:
```bash
python manage.py runserver
```


### doc Swagger e redoc
```bash
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/
```


## 📁 Estrutura do Projeto
iaeco-backend/
├── core/
│   ├── settings.py       # Configurações do Django
│   ├── urls.py          # Rotas principais da API
│   ├── celery.py        # Configuração do Celery
│   ├── wsgi.py          # Configuração WSGI
├── home/
│   ├── admin.py         # Configuração do Django Admin
│   ├── models.py        # Modelos (CustomUser, Company, DocumentUpload, etc.)
│   ├── serializers.py   # Serializers para a API
│   ├── views.py         # Views e ViewSets da API
│   ├── tasks.py         # Tarefas do Celery
│   ├── apps.py          # Configuração do app
├── media/               # Arquivos de upload (ex.: documentos)
├── static/              # Arquivos estáticos coletados
├── .env                 # Configurações locais (não versionado)
├── .env-example         # Exemplo de variáveis de ambiente
├── .gitignore           # Arquivos/diretórios ignorados pelo Git
├── manage.py            # Script de gerenciamento do Django
├── requirements.txt     # Dependências do projeto
├── README.md            # Este documento


## 🛠️ Tecnologias e Ferramentas

 - Django — Framework web para desenvolvimento rápido e seguro
 - Django REST Framework — Toolkit para construção de APIs REST
 - Celery — Sistema de filas para tarefas assíncronas
 - RabbitMQ — Broker de mensagens para o Celery
 - Redis — Armazenamento de resultados do Celery
 - PostgreSQL — Banco de dados relacional
 - GHG Protocol — Framework para contabilização de emissões de carbono
 - django-auditlog — Auditoria de ações no sistema
 - drf-yasg — Geração de documentação Swagger para a API


## 🌍 Sobre o IaEco

O IaEco ajuda organizações e indivíduos a identificar, categorizar e monitorar suas emissões de carbono com base em atividades que se encaixam nos escopos e categorias do GHG Protocol. A API backend gerencia autenticação, uploads de documentos, processamento de dados e geração de métricas para o dashboard do frontend, promovendo transparência climática e ações sustentáveis.


## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.


## 💡 Dicas para Desenvolvimento

 - Documentação da API: Acesse http://localhost:8000/api/v1/swagger/ para explorar os endpoints (requer drf-yasg).

 - Depuração: Ative logs detalhados em core/settings.py para troubleshoot.

 - Produção: Configure DEBUG=False, HTTPS, e use gunicorn com supervisord para Celery.

 - Testes: Adicione testes unitários em home/tests.py e execute com python manage.py test.