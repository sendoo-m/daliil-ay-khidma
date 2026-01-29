"""
Review Reply Form
"""

from django import forms

try:
    from apps.reviews.models import Review
    REVIEWS_AVAILABLE = True
except ImportError:
    REVIEWS_AVAILABLE = False
    # Create dummy class
    class Review:
        pass


class ReviewReplyForm(forms.ModelForm):
    """Review Reply Form"""
    
    class Meta:
        model = Review
        fields = ['reply']
        
        widgets = {
            'reply': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'اكتب ردك على التقييم...',
                'dir': 'rtl'
            }),
        }
        
        labels = {
            'reply': 'الرد',
        }
