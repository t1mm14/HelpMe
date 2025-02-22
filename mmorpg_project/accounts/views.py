from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib import messages
from django.views import View
from .models import EmailVerification

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('advertisement_list')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('advertisement_list')
    http_method_names = ['get', 'post']  # Разрешаем GET-запросы

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        
        # Генерация кода подтверждения
        confirmation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        user.confirmation_code = confirmation_code
        user.save()
        
        # Отправка email с кодом подтверждения
        send_mail(
            'Подтверждение регистрации',
            f'Ваш код подтверждения: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return redirect('confirm_email') 

class EmailVerificationView(View):
    def get(self, request):
        return render(request, 'accounts/verify_email.html')
        
    def post(self, request):
        code = request.POST.get('code')
        try:
            verification = EmailVerification.objects.get(
                verification_code=code,
                user__email=request.session.get('verification_email')
            )
            user = verification.user
            user.is_active = True
            user.save()
            verification.delete()
            messages.success(request, 'Email успешно подтвержден!')
            return redirect('login')
        except EmailVerification.DoesNotExist:
            messages.error(request, 'Неверный код подтверждения')
            return redirect('verify_email') 