"""Custom Authentication Classes"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.authentication import SessionAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT Authentication with better error handling"""
    
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except InvalidToken as e:
            # Log the error or handle it
            return None


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Session authentication without CSRF for API"""
    
    def enforce_csrf(self, request):
        return  # Skip CSRF check for API
