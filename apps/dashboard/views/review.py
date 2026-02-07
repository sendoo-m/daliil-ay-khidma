"""
Review Management Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

try:
    from apps.reviews.models import Review
    REVIEWS_AVAILABLE = True
except ImportError:
    REVIEWS_AVAILABLE = False

from apps.dashboard.forms import ReviewReplyForm


@login_required
def review_list(request):
    """قائمة تقييمات محلات المستخدم"""
    if not REVIEWS_AVAILABLE:
        messages.warning(request, 'نظام التقييمات غير متوفر حالياً')
        return redirect('dashboard:home')
    
    reviews = Review.objects.filter(
        business__owner=request.user
    ).select_related('business', 'user').order_by('-created_at')
    
    # Filter by business
    business_id = request.GET.get('business')
    if business_id:
        reviews = reviews.filter(business_id=business_id)
    
    # Filter by rating
    rating = request.GET.get('rating')
    if rating:
        reviews = reviews.filter(rating=rating)
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'approved':
        reviews = reviews.filter(is_approved=True)
    elif status == 'pending':
        reviews = reviews.filter(is_approved=False)
    elif status == 'replied':
        reviews = reviews.filter(reply__isnull=False).exclude(reply='')
    elif status == 'unreplied':
        reviews = reviews.filter(Q(reply__isnull=True) | Q(reply=''))
    
    # Search
    search = request.GET.get('search')
    if search:
        reviews = reviews.filter(
            Q(comment__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(reviews, 15)
    page = request.GET.get('page')
    reviews = paginator.get_page(page)
    
    # Get user businesses for filter
    from apps.directory.models import Business
    businesses = Business.objects.filter(owner=request.user)
    
    context = {
        'reviews': reviews,
        'businesses': businesses,
        'total_count': Review.objects.filter(business__owner=request.user).count(),
        'pending_count': Review.objects.filter(
            business__owner=request.user,
            is_approved=False
        ).count(),
        'unreplied_count': Review.objects.filter(
            business__owner=request.user
        ).filter(Q(reply__isnull=True) | Q(reply='')).count(),
    }
    
    return render(request, 'dashboard/review/list.html', context)


@login_required
def review_reply(request, pk):
    """الرد على تقييم"""
    if not REVIEWS_AVAILABLE:
        messages.warning(request, 'نظام التقييمات غير متوفر حالياً')
        return redirect('dashboard:home')
    
    review = get_object_or_404(Review, pk=pk, business__owner=request.user)
    
    if request.method == 'POST':
        form = ReviewReplyForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إضافة الرد بنجاح!')
            return redirect('dashboard:review_list')
    else:
        form = ReviewReplyForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
    }
    
    return render(request, 'dashboard/review/reply.html', context)
