"""
Custom middleware for Daliil Ay Khidma
"""
from django.utils import translation
from django.conf import settings


class AdminEnglishMiddleware:
    """
    Force Django Admin to use English language only.
    All other pages will use Arabic (default language).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is accessing admin panel
        if request.path.startswith('/admin'):
            # Force English for admin panel
            translation.activate('en')
            request.LANGUAGE_CODE = 'en'
        else:
            # Use Arabic for all other pages (default language)
            translation.activate('ar')
            request.LANGUAGE_CODE = 'ar'
        
        response = self.get_response(request)
        
        # Deactivate to prevent thread issues
        translation.deactivate()
        
        return response


class ForceArabicMiddleware:
    """
    Force all non-admin pages to use Arabic language.
    This middleware ensures consistent Arabic experience across the site.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip admin panel (handled by AdminEnglishMiddleware)
        if not request.path.startswith('/admin'):
            # Set Arabic as active language
            translation.activate('ar')
            request.LANGUAGE_CODE = 'ar'
        
        response = self.get_response(request)
        return response
