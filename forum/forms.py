from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comentario

# -----------------------------
# Formulário de Comentários
# -----------------------------
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deixe seu comentário...'
            })
        }

# -----------------------------
# Formulário de Registro com E-mail e validação
# -----------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Digite seu e-mail"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email").strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.is_active = False  # 🔒 Conta aguardando aprovação
        if commit:
            user.save()
        return user
