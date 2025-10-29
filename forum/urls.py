from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('pesquisar/', views.pesquisar_videos, name='pesquisar_videos'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('excluir-conta/', views.excluir_conta, name='excluir_conta'),
    path('register/', views.register, name='register'),
]
