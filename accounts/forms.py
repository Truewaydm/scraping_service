from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()
        if email and password:
            query_set = User.objects.filter(email=email)
            if not query_set.exists():
                raise forms.ValidationError('This username not found!')
            if not check_password(password, query_set[0].password):
                raise forms.ValidationError('Invalid password!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('This user is inactive')
        return super(UserLoginForm, self).clean(*args, **kwargs)
