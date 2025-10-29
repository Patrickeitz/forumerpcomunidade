from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.urls import path

from .models import Video, Comentario


# ---------------------------
# 🧠 Função de envio de e-mail de aprovação
# ---------------------------
def enviar_email_aprovacao(user):
    assunto = "✅ Sua conta foi aprovada!"
    mensagem = (
        f"Olá {user.username},\n\n"
        "Sua conta no Fórum ERP Comunidade foi aprovada com sucesso! 🎉\n\n"
        "Agora você já pode acessar e participar das discussões no fórum:\n"
        "👉 http://127.0.0.1:8000/\n\n"
        "Atenciosamente,\nEquipe do Fórum ERP Comunidade"
    )
    try:
        send_mail(
            subject=assunto,
            message=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        print(f"📩 E-mail de aprovação enviado para: {user.email}")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar e-mail de aprovação: {e}")


# ---------------------------
# ⚙️ Painel de Administração Customizado
# ---------------------------
class CustomAdminSite(admin.AdminSite):
    site_header = "Painel do Fórum ERP"
    site_title = "Administração Fórum ERP"
    index_title = "Gerenciamento do Fórum"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'aprovar_usuario/<int:user_id>/',
                self.admin_view(self.aprovar_usuario),
                name='aprovar_usuario'
            ),
        ]
        return custom_urls + urls

    def aprovar_usuario(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        if not user.is_active:
            user.is_active = True
            user.save()
            enviar_email_aprovacao(user)
            messages.success(
                request, f"O usuário {user.username} foi aprovado e notificado por e-mail."
            )
        else:
            messages.info(request, f"O usuário {user.username} já estava ativo.")

        return redirect('/painel/auth/user/')


# Instância do painel customizado
admin_site = CustomAdminSite(name='custom_admin')


# ---------------------------
# 👤 Custom User Admin
# ---------------------------
@admin.register(User, site=admin_site)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'data_cadastro', 'acoes_aprovacao')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    def data_cadastro(self, obj):
        return obj.date_joined.strftime("%d/%m/%Y %H:%M")
    data_cadastro.short_description = "Cadastrado em"

    def acoes_aprovacao(self, obj):
        if not obj.is_active:
            return format_html(
                '<a class="button" href="/painel/aprovar_usuario/{}/" '
                'style="background-color:#28a745;color:white;padding:5px 10px;'
                'border-radius:5px;text-decoration:none;">Aprovar ✅</a>',
                obj.id
            )
        return "Ativo ✅"
    acoes_aprovacao.short_description = "Aprovação"


# ---------------------------
# 🎞️ Admin do Fórum
# ---------------------------
@admin.register(Video, site=admin_site)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'disponivel', 'publicado_em', 'exibir_thumbnail')
    list_filter = ('disponivel', 'publicado_em')
    search_fields = ('titulo', 'descricao')

    def exibir_thumbnail(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="100" height="56" style="object-fit:cover;">', obj.thumbnail.url)
        return "—"
    exibir_thumbnail.short_description = "Miniatura"


@admin.register(Comentario, site=admin_site)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('video', 'usuario', 'criado_em')
    search_fields = ('usuario__username', 'texto')
    list_filter = ('criado_em',)
