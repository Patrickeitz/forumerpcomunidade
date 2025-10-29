import os
import subprocess
import platform
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Video(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)
    publicado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Salva o vídeo primeiro

        # Verifica se o vídeo existe e ainda não tem thumbnail
        if self.arquivo and not self.thumbnail:
            try:
                input_path = self.arquivo.path
                output_dir = os.path.join(os.path.dirname(input_path), 'thumbs')
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{self.id}_thumb.jpg")

                # Caminho do ffmpeg
                if 'pythonanywhere' in platform.platform().lower():
                    ffmpeg_path = '/home/seu_usuario/ffmpeg/ffmpeg'  # será ajustado depois no deploy
                else:
                    ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe'  # caminho fixo para Windows

                # Extrai o frame do vídeo
                command = [
                    ffmpeg_path, '-i', input_path,
                    '-ss', '00:00:02',  # pega o frame no segundo 2
                    '-vframes', '1', output_path
                ]
                subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

                # Atualiza o campo thumbnail no modelo
                rel_path = os.path.relpath(output_path, os.path.join(os.path.dirname(input_path), '..'))
                self.thumbnail = os.path.join('videos', 'thumbs', os.path.basename(output_path)).replace('\\', '/')
                super().save(update_fields=['thumbnail'])

            except Exception as e:
                print(f"Erro ao gerar thumbnail: {e}")

class Comentario(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.video.titulo}"
