from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bienvenido {username}!')
                return redirect('finanzas:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'autentication/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f'Cuenta creada exitosamente! Bienvenido {user.username}!')
            return redirect('autentication/home.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'autentication/register.html', {'form': form})

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña ha sido actualizada!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'autentication/password_change.html', {'form': form})

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Recuperación de contraseña"
                    email_template_name = "autentications/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Control Gestión Cacciuttolo',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject, 
                            email, 
                            settings.DEFAULT_FROM_EMAIL, 
                            [user.email], 
                            fail_silently=False
                        )
                        messages.success(request, 'Se ha enviado un email con instrucciones para recuperar tu contraseña.')
                        return redirect('login')
                    except Exception as e:
                        messages.error(request, f'Error al enviar el email: {str(e)}')
                        return redirect('password_reset')
            messages.error(request, 'No existe una cuenta con ese email.')
    form = PasswordResetForm()
    return render(request, 'autentications/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tu contraseña ha sido actualizada. Ahora puedes iniciar sesión.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'autentications/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'El enlace de recuperación de contraseña es inválido o ha expirado.')
        return redirect('password_reset') 