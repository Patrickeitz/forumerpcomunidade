# ☕ Fórum ERP Comunidade

Um sistema de fórum desenvolvido em **Django**, com foco em **colaboração e troca de conhecimento entre usuários de ERP**.  
O projeto foi criado como parte de um estudo sobre **desenvolvimento web com Python/Django**.

---

## 🚀 Tecnologias

- **Django 4.2+**
- **SQLite3**
- **Bootstrap 5**
- **FFmpeg / MoviePy** (para manipulação de mídia)
- **PythonAnywhere** (deploy)

---

## ⚙️ Instalação local

```bash
# Clone o repositório
git clone https://github.com/Patrickeitz/forumerpcomunidade.git
cd forumerpcomunidade

# Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate  # (Windows)
source venv/bin/activate  # (Linux/Mac)

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
Acesse em: http://localhost:8000

🌐 Deploy no PythonAnywhere
Clone o projeto na sua conta PythonAnywhere

Configure o WSGI com o arquivo wsgi_pythonanywhere.py

Execute:

bash
Copiar código
python manage.py migrate
python manage.py collectstatic
Clique em Reload no painel “Web”

📷 Funcionalidades Principais
Cadastro e autenticação de usuários

Criação de tópicos e respostas

Sistema de mídia com suporte a vídeos (via FFmpeg)

Painel administrativo do Django

Layout responsivo com Bootstrap

💡 Autor
Patrick Eitz
📘 Projeto: Fórum ERP Comunidade
🔗 https://github.com/Patrickeitz/forumerpcomunidade

✨ Desenvolvido com Django, café e dedicação!

---

## 🔄 3️⃣ — Atualizar tudo no GitHub

Depois de salvar os 3 arquivos (`requirements.txt`, `wsgi_pythonanywhere.py`, `README.md`), execute no terminal do VS Code:

```bash
git add .
git commit -m "Adicionados requirements.txt, WSGI e README.md aprimorado"
git push
