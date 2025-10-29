from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def notificar_admin_novo_usuario(sender, instance, created, **kwargs):
    """
    Envia e-mail apenas quando um novo usuário é criado inativo.
    Não envia e-mail quando o admin ativa o usuário.
    """

    # 🆕 Novo usuário criado e inativo
    if created and not instance.is_active:
        assunto_admin = "🆕 Novo usuário aguardando aprovação"
        mensagem_admin = (
            f"Um novo usuário se registrou e está aguardando aprovação.\n\n"
            f"Usuário: {instance.username}\n"
            f"E-mail: {instance.email}\n\n"
            f"Acesse o painel administrativo para aprovar o cadastro:\n"
            f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}/admin/auth/user/"
        )

        try:
            send_mail(
                subject=assunto_admin,
                message=mensagem_admin,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print(f"📩 E-mail enviado ao admin sobre o novo usuário: {instance.username}")
        except Exception as e:
            print(f"⚠️ Erro ao enviar e-mail ao admin: {e}")
