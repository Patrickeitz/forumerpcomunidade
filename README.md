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
