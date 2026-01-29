"""
Subscriptions Views
===================
عرض وإدارة الاشتراكات والخطط
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta

from .models import SubscriptionPlan, Subscription
from apps.directory.models import Business


# ========================================
# Public Views
# ========================================

def plans_list(request):
    """
    عرض جميع خطط الاشتراك
    """
    plans = SubscriptionPlan.objects.filter(
        is_active=True
    ).order_by('order', 'price_monthly')
    
    context = {
        'plans': plans,
    }
    
    return render(request, 'subscriptions/plans_list.html', context)


def plan_detail(request, plan_name):
    """
    تفاصيل خطة محددة
    """
    plan = get_object_or_404(
        SubscriptionPlan,
        name=plan_name,
        is_active=True
    )
    
    # Get other plans for comparison
    other_plans = SubscriptionPlan.objects.filter(
        is_active=True
    ).exclude(name=plan_name).order_by('order')
    
    context = {
        'plan': plan,
        'other_plans': other_plans,
    }
    
    return render(request, 'subscriptions/plan_detail.html', context)


def pricing_comparison(request):
    """
    صفحة مقارنة الأسعار والميزات
    """
    plans = SubscriptionPlan.objects.filter(
        is_active=True
    ).order_by('order', 'price_monthly')
    
    context = {
        'plans': plans,
    }
    
    return render(request, 'subscriptions/pricing_comparison.html', context)


# ========================================
# Subscription Management
# ========================================

@login_required
def my_subscription(request):
    """
    اشتراك المستخدم الحالي
    """
    try:
        business = Business.objects.get(owner=request.user)
        
        try:
            subscription = Subscription.objects.select_related('plan').get(
                business=business
            )
        except Subscription.DoesNotExist:
            subscription = None
        
    except Business.DoesNotExist:
        business = None
        subscription = None
    
    # Get available plans
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('order')
    
    context = {
        'business': business,
        'subscription': subscription,
        'plans': plans,
    }
    
    return render(request, 'subscriptions/my_subscription.html', context)


@login_required
def subscribe(request, plan_name):
    """
    الاشتراك في خلطة محددة
    """
    # Check if user has business
    try:
        business = Business.objects.get(owner=request.user)
    except Business.DoesNotExist:
        messages.error(request, 'يجب إنشاء محل أولاً قبل الاشتراك')
        return redirect('dashboard:dashboard')
    
    # Get plan
    plan = get_object_or_404(
        SubscriptionPlan,
        name=plan_name,
        is_active=True
    )
    
    # Check if already subscribed
    existing_sub = Subscription.objects.filter(business=business).first()
    
    if request.method == 'POST':
        duration = request.POST.get('duration', 'monthly')
        
        # Calculate dates
        start_date = timezone.now()
        
        duration_days = {
            'monthly': 30,
            'quarterly': 90,
            'semi_annual': 180,
            'annual': 365,
        }
        
        end_date = start_date + timedelta(days=duration_days.get(duration, 30))
        
        # Calculate price
        amount = plan.get_price(duration)
        
        # If existing subscription, update it
        if existing_sub:
            existing_sub.plan = plan
            existing_sub.start_date = start_date
            existing_sub.end_date = end_date
            existing_sub.amount_paid = amount
            existing_sub.status = 'pending'  # Waiting for payment
            existing_sub.save()
            subscription = existing_sub
        else:
            # Create new subscription
            subscription = Subscription.objects.create(
                business=business,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                amount_paid=amount,
                status='pending'  # Waiting for payment
            )
        
        # Here you would integrate with payment gateway
        # For now, we'll just redirect to payment page
        
        messages.success(
            request,
            f'تم إنشاء طلب الاشتراك في {plan.display_name}. '
            f'يرجى إتمام عملية الدفع.'
        )
        
        return redirect('subscriptions:payment', subscription_id=subscription.id)
    
    context = {
        'plan': plan,
        'business': business,
        'existing_sub': existing_sub,
    }
    
    return render(request, 'subscriptions/subscribe.html', context)


@login_required
def payment(request, subscription_id):
    """
    صفحة الدفع
    """
    subscription = get_object_or_404(
        Subscription.objects.select_related('plan', 'business'),
        id=subscription_id,
        business__owner=request.user
    )
    
    if request.method == 'POST':
        # Here integrate with payment gateway
        # For now, we'll simulate successful payment for free plans
        
        payment_method = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id', '')
        
        # If free plan, activate immediately
        if subscription.amount_paid == 0:
            subscription.status = 'active'
            subscription.payment_method = 'free'
            subscription.save()
            
            messages.success(request, 'تم تفعيل اشتراكك بنجاح!')
            return redirect('subscriptions:my_subscription')
        else:
            # For paid plans, mark as pending until admin confirms
            subscription.payment_method = payment_method
            subscription.transaction_id = transaction_id
            subscription.save()
            
            messages.info(
                request,
                'تم إرسال بيانات الدفع. سيتم تفعيل اشتراكك '
                'بعد التحقق من الدفع.'
            )
            return redirect('subscriptions:my_subscription')
    
    context = {
        'subscription': subscription,
    }
    
    return render(request, 'subscriptions/payment.html', context)


@login_required
@require_POST
def cancel_subscription(request):
    """
    إلغاء الاشتراك
    """
    try:
        business = Business.objects.get(owner=request.user)
        subscription = Subscription.objects.get(business=business)
        
        subscription.cancel()
        
        messages.success(request, 'تم إلغاء الاشتراك بنجاح')
        
    except (Business.DoesNotExist, Subscription.DoesNotExist):
        messages.error(request, 'لم يتم العثور على اشتراك نشط')
    
    return redirect('subscriptions:my_subscription')


@login_required
@require_POST
def toggle_auto_renew(request):
    """
    تفعيل/تعطيل التجديد التلقائي
    """
    try:
        business = Business.objects.get(owner=request.user)
        subscription = Subscription.objects.get(business=business)
        
        subscription.auto_renew = not subscription.auto_renew
        subscription.save()
        
        if subscription.auto_renew:
            messages.success(request, 'تم تفعيل التجديد التلقائي')
        else:
            messages.success(request, 'تم تعطيل التجديد التلقائي')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'auto_renew': subscription.auto_renew
            })
        
    except (Business.DoesNotExist, Subscription.DoesNotExist):
        messages.error(request, 'لم يتم العثور على اشتراك نشط')
    
    return redirect('subscriptions:my_subscription')


@login_required
def upgrade_subscription(request, plan_name):
    """
    ترقية الاشتراك
    """
    try:
        business = Business.objects.get(owner=request.user)
        current_sub = Subscription.objects.get(business=business)
    except (Business.DoesNotExist, Subscription.DoesNotExist):
        messages.error(request, 'يجب أن يكون لديك اشتراك حالي')
        return redirect('subscriptions:plans_list')
    
    new_plan = get_object_or_404(
        SubscriptionPlan,
        name=plan_name,
        is_active=True
    )
    
    # Check if it's actually an upgrade
    if new_plan.price_monthly <= current_sub.plan.price_monthly:
        messages.warning(request, 'يرجى اختيار خطة أعلى')
        return redirect('subscriptions:plans_list')
    
    if request.method == 'POST':
        # Calculate prorated amount (simplified)
        # In real app, you'd calculate the remaining days and charge accordingly
        
        current_sub.plan = new_plan
        current_sub.save()
        
        messages.success(
            request,
            f'تمت ترقية اشتراكك إلى {new_plan.display_name} بنجاح!'
        )
        return redirect('subscriptions:my_subscription')
    
    context = {
        'current_sub': current_sub,
        'new_plan': new_plan,
    }
    
    return render(request, 'subscriptions/upgrade.html', context)


# ========================================
# AJAX Views
# ========================================

def get_plan_price(request, plan_name, duration):
    """
    الحصول على سعر خطة حسب المدة (AJAX)
    """
    try:
        plan = SubscriptionPlan.objects.get(name=plan_name)
        price = plan.get_price(duration)
        
        return JsonResponse({
            'success': True,
            'price': float(price),
            'plan_name': plan.display_name
        })
    except SubscriptionPlan.DoesNotExist:
        return JsonResponse({'success': False}, status=404)
