from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db.models import Q

from .models import Video
from .forms import ComentarioForm, CustomUserCreationForm
from django.contrib.auth.models import User


# ======================
# PÁGINA INICIAL
# ======================
def index(request):
    videos = Video.objects.filter(disponivel=True).order_by('-publicado_em')
    return render(request, 'index.html', {'videos': videos})


# ======================
# SOBRE
# ======================
def sobre(request):
    return render(request, 'sobre.html')


# ======================
# CONTATO (envio de e-mail)
# ======================
def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto') or 'Informação sobre o Fórum'
        mensagem = request.POST.get('mensagem')

        if not (nome and email and mensagem):
            messages.error(request, 'Preencha todos os campos do formulário.')
            return render(request, 'contato.html')

        corpo_email = (
            f"Nova mensagem de contato:\n\n"
            f"Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\n\nMensagem:\n{mensagem}"
        )

        try:
            send_mail(
                subject=f"[Contato] {assunto}",
                message=corpo_email,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except BadHeaderError:
            messages.error(request, "Erro: cabeçalho de e-mail inválido.")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            messages.error(request, "Erro ao enviar a mensagem. Verifique as configurações de e-mail.")
        else:
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect('contato')

    return render(request, 'contato.html')


# ======================
# DETALHE DO VÍDEO + COMENTÁRIOS
# ======================
@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comentarios = video.comentarios.all()
    form = ComentarioForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comentario = form.save(commit=False)
        comentario.video = video
        comentario.usuario = request.user
        comentario.save()
        messages.success(request, 'Comentário enviado!')
        return redirect('video_detail', video_id=video.id)
    return render(request, 'video_detail.html', {
        'video': video,
        'comentarios': comentarios,
        'form': form
    })


# ======================
# REGISTRO DE USUÁRIO
# ======================
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            # Verifica se o username já existe
            user_by_username = User.objects.filter(username=username).first()
            if user_by_username:
                if not user_by_username.is_active:
                    # Reativa usuário inativo
                    user_by_username.set_password(password)
                    user_by_username.email = email
                    user_by_username.is_active = False
                    user_by_username.save()  # post_save signal enviará e-mail
                    messages.success(
                        request,
                        "Conta reativada e aguardando aprovação do administrador!"
                    )
                    return redirect('login')
                else:
                    messages.error(request, "Usuário já existe!")
                    return redirect('register')
            
            # Cria novo usuário inativo
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False
            )
            # NÃO chamamos enviar_email_admin(user) aqui
            messages.success(
                request,
                "Conta criada! Aguarde aprovação do administrador."
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# Função para enviar e-mail ao admin
def enviar_email_admin(user):
    try:
        send_mail(
            subject=f"Novo usuário aguardando aprovação: {user.username}",
            message=(
                f"Um novo usuário se registrou no Fórum ERP Comunidade:\n\n"
                f"Usuário: {user.username}\n"
                f"E-mail: {user.email}\n\n"
                "Acesse o painel administrativo para aprovar a conta."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        print(f"📩 E-mail enviado ao admin sobre o novo usuário: {user.username}")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail para admin: {e}")


# ======================
# LOGIN CUSTOMIZADO (bloqueia não aprovados)
# ======================
def custom_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Bem-vindo(a), {user.username}!")
                    return redirect("index")
                else:
                    messages.warning(
                        request,
                        "⚠️ Sua conta ainda não foi aprovada pelo administrador. "
                        "Você receberá um e-mail quando for liberada."
                    )
                    return redirect("login")
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Verifique os dados informados e tente novamente.")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


# ======================
# MINHA CONTA / EXCLUIR CONTA
# ======================
@login_required
def minha_conta(request):
    return render(request, 'minha_conta.html')


@login_required
def excluir_conta(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Sua conta foi excluída com sucesso.")
        return redirect('index')
    return render(request, 'excluir_conta_confirm.html', {'user': request.user})


# ======================
# PESQUISA DE VÍDEOS 🔍
# ======================
def pesquisar_videos(request):
    query = request.GET.get('q', '')
    videos = Video.objects.filter(
        Q(titulo__icontains=query) | Q(descricao__icontains=query),
        disponivel=True
    ).order_by('-publicado_em')
    return render(request, 'pesquisa_resultados.html', {
        'videos': videos,
        'query': query
    })
