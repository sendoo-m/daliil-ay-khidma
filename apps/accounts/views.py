"""
Account Views
=============
واجهات المستخدم للحسابات: التسجيل، الدخول، الملف الشخصي
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    PasswordResetView as BasePasswordResetView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)

from .models import User
from .forms import (
    RegistrationForm,
    LoginForm,
    ProfileUpdateForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)


# ========================================
# Registration View
# ========================================
class RegisterView(CreateView):
    """عرض التسجيل"""
    model = User
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تم إنشاء حسابك بنجاح! يمكنك الآن تسجيل الدخول.')
        return response
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().get(request, *args, **kwargs)


# ========================================
# Login View
# ========================================
class LoginView(BaseLoginView):
    """عرض تسجيل الدخول"""
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('dashboard:home')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'مرحباً {username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'اسم المستخدم أو كلمة المرور غير صحيحة!')
        return super().form_invalid(form)


# ========================================
# Logout View
# ========================================
class LogoutView(View):
    """عرض تسجيل الخروج"""
    
    def get(self, request):
        logout(request)
        messages.success(request, 'تم تسجيل الخروج بنجاح')
        return redirect('accounts:login')
    
    def post(self, request):
        logout(request)
        messages.success(request, 'تم تسجيل الخروج بنجاح')
        return redirect('accounts:login')


# ========================================
# Profile View
# ========================================
@login_required
def profile_view(request):
    """عرض وتحديث الملف الشخصي"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث ملفك الشخصي بنجاح!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)


# ========================================
# Password Change View
# ========================================
@login_required
def password_change_view(request):
    """تغيير كلمة المرور"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'تم تغيير كلمة المرور بنجاح!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {'form': form}
    return render(request, 'accounts/password_change.html', context)


# ========================================
# Password Reset Views
# ========================================
class PasswordResetView(BasePasswordResetView):
    """إرسال رابط استرجاع كلمة المرور"""
    form_class = PasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(BasePasswordResetDoneView):
    """تم إرسال رابط استرجاع كلمة المرور"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    """إدخال كلمة مرور جديدة"""
    form_class = SetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    """تم استرجاع كلمة المرور بنجاح"""
    template_name = 'accounts/password_reset_complete.html'
