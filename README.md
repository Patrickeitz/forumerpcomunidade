<h1 align="center">☕ Fórum ERP Comunidade</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-5.2-green.svg?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" />
</p>

<p align="center">
  <b>Plataforma de discussão e colaboração entre usuários de sistemas ERP.</b><br>
  Projeto acadêmico desenvolvido com <b>Django</b>, <b>Bootstrap</b> e <b>FFmpeg</b>.
</p>

---

## 🚀 Como Rodar o Projeto Localmente (Windows)

### 🔧 Pré-requisitos
Antes de começar, instale:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [FFmpeg](https://ffmpeg.org/download.html) — (necessário para recursos de vídeo e áudio)

---

### 🧩 Passo a Passo

#### 1️⃣ Clone o repositório
```bash
git clone https://github.com/Patrickeitz/forumerpcomunidade.git
cd forumerpcomunidade

2️⃣ Crie e ative o ambiente virtual
python -m venv venv
Windows:
venv\Scripts\activate

Linux:
source venv/bin/activate

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Execute as migrações
python manage.py migrate

5️⃣ Inicie o servidor
python manage.py runserver

📍 Acesse o projeto no navegador:
👉 http://127.0.0.1:8000/

🧠 Tecnologias Utilizadas
Categoria	Tecnologia
Backend	Django 5.2
Banco de dados	SQLite3
Frontend	HTML, CSS, Bootstrap 5
Uploads e mídia	Pillow, FFmpeg
Outras libs	django-filter, django-widget-tweaks, python-decouple

⚙️ Arquivo .env
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

DEBUG=True
SECRET_KEY=sua_chave_secreta_aqui
ALLOWED_HOSTS=127.0.0.1,localhost
📁 Estrutura do Projeto

projetoforum/
├── core/                # Configurações principais do Django
├── forum/               # Aplicativo principal (tópicos, postagens, etc.)
├── templates/           # Páginas HTML
├── static/              # CSS, JS e Bootstrap
├── media/               # Uploads de usuários
├── db.sqlite3           # Banco de dados local
├── manage.py            # Comando principal do Django
└── requirements.txt     # Dependências do projeto

✨ Recursos do Sistema
✅ Cadastro e autenticação de usuários
✅ Criação de tópicos e respostas
✅ Upload de imagens e vídeos (via FFmpeg)
✅ Painel administrativo completo
✅ Interface moderna e responsiva com Bootstrap

💡 Dicas Úteis
Criar um superusuário:

python manage.py createsuperuser

Acessar o painel admin:
http://127.0.0.1:8000/admin

Caso precise recriar migrações:

del /s /q forum\migrations\*.py
python manage.py makemigrations
python manage.py migrate

🧑‍💻 Autor
Patrick Eitz
📘 Projeto: Fórum ERP Comunidade
🌐 GitHub: @Patrickeitz
💬 “Compartilhar conhecimento é evoluir junto.”

<p align="center"> Feito com ❤️ e ☕ usando <b>Django</b>. </p> ```
