"""
API Permissions
===============
Custom permissions for API endpoints
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners to edit objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to owner
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'business'):
            return obj.business.owner == request.user
        
        return False


class IsBusinessOwner(permissions.BasePermission):
    """
    Permission to check if user owns the business
    """
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'business'):
            return obj.business.owner == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False
