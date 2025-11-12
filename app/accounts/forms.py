from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class':'w-full border rounded px-3 py-2'})
    )
    confirm_password = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class':'w-full border rounded px-3 py-2'})
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        labels = {
            'email': 'Correo electrónico',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class':'w-full border rounded px-3 py-2'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password != confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ensure fields have consistent Tailwind classes if rendered individually
        for fname, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class':'w-full border rounded px-3 py-2'})
