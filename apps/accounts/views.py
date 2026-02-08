"""
Accounts Views
==============
Views for user authentication
"""

from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache


@never_cache
@require_http_methods(["GET", "POST"])
def login_view(request):
    """صفحة تسجيل الدخول"""
    
    # If already logged in, redirect based on role
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard:home')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'الرجاء إدخال اسم المستخدم وكلمة المرور')
            return render(request, 'accounts/login.html')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            login(request, user)
            messages.success(request, f'مرحباً بك {user.get_full_name() or user.username}!')
            
            # Redirect based on role
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            elif user.is_staff or user.is_superuser:
                return redirect('admin_dashboard:home')
            else:
                return redirect('dashboard:home')
        else:
            # Authentication failed
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render(request, 'accounts/login.html')


class LogoutView(DjangoLogoutView):
    """صفحة تسجيل الخروج"""
    http_method_names = ['get', 'post', 'options']
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
