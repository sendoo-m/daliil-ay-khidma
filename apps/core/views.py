# apps/core/views.py
from django.shortcuts import render
from apps.directory.models import Category, Business
from apps.deals.models import Deal


def home(request):
    """الصفحة الرئيسية"""
    context = {
        'featured_businesses': Business.objects.filter(
            is_active=True,
            is_verified=True,
            is_featured=True
        )[:6],
        'categories': Category.objects.filter(
            is_active=True,
            parent__isnull=True
        ).order_by('order')[:8],
        'active_deals': Deal.objects.filter(
            is_active=True
        ).order_by('-created_at')[:4],
    }
    return render(request, 'core/home.html', context)


def about(request):
    """صفحة من نحن"""
    return render(request, 'core/about.html')


def contact(request):
    """صفحة اتصل بنا"""
    return render(request, 'core/contact.html')
