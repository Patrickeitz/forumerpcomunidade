from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from forum.admin import admin_site  # 👉 Importa o painel customizado
from forum.views import custom_login_view  # 👈 login customizado


def custom_logout_view(request):
    """Efetua logout via POST e exibe mensagem de sucesso."""
    if request.method == "POST":
        logout(request)
        messages.success(request, "Você saiu com sucesso.")
        return redirect('index')
    else:
        messages.error(request, "Logout deve ser feito via POST.")
        return redirect('index')


urlpatterns = [
    path('painel/', admin_site.urls),  # 👉 Usa apenas o painel customizado
    path('', include('forum.urls')),

    # Login customizado
    path('conta/login/', custom_login_view, name='login'),

    # Autenticação padrão (senha, redefinição etc.)
    path('conta/', include('django.contrib.auth.urls')),

    # Logout via POST
    path('logout/', custom_logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
