"""
Reviews Serializers
===================
Serializers for Reviews (if reviews app exists)
"""

from rest_framework import serializers

try:
    from apps.reviews.models import Review
    
    class ReviewSerializer(serializers.ModelSerializer):
        """Review Serializer"""
        user_name = serializers.CharField(source='user.get_full_name', read_only=True)
        
        class Meta:
            model = Review
            fields = '__all__'
            read_only_fields = ['user', 'is_approved', 'created_at']
            
except ImportError:
    # Reviews app doesn't exist yet
    pass
