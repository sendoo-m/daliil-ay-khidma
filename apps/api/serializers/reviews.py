"""
Reviews Serializers
===================
Serializers for Reviews (if reviews app exists)
"""

"""
Reviews Serializers
===================
"""

from rest_framework import serializers

try:
    from apps.reviews.models import Review

    class ReviewSerializer(serializers.ModelSerializer):
        """Review Serializer - للعرض"""
        user_name = serializers.CharField(source='user.get_full_name', read_only=True)
        user_username = serializers.CharField(source='user.username', read_only=True)
        business_name = serializers.CharField(source='business.name_ar', read_only=True)

        class Meta:
            model = Review
            fields = '__all__'
            read_only_fields = ['user', 'is_approved', 'approved_at', 'approved_by', 'created_at', 'updated_at']

    class ReviewCreateSerializer(serializers.ModelSerializer):
        """Review Create/Update Serializer"""

        class Meta:
            model = Review
            fields = ['business', 'rating', 'comment']

        def validate_rating(self, value):
            if not 1 <= value <= 5:
                raise serializers.ValidationError("التقييم يجب أن يكون بين 1 و 5")
            return value

        def validate(self, attrs):
            request = self.context.get('request')
            business = attrs.get('business')

            # منع المستخدم من تقييم محله الخاص
            if request and business and hasattr(business, 'owner'):
                if business.owner == request.user:
                    raise serializers.ValidationError("لا يمكنك تقييم محلك الخاص")

            # منع تكرار التقييم
            if request and business:
                existing = Review.objects.filter(
                    user=request.user,
                    business=business
                )
                # استثناء حالة التعديل
                if self.instance:
                    existing = existing.exclude(pk=self.instance.pk)
                if existing.exists():
                    raise serializers.ValidationError("لقد قمت بتقييم هذا المحل مسبقاً")

            return attrs

except ImportError:
    pass

# from rest_framework import serializers
# from apps.reviews.models import Review


# class ReviewSerializer(serializers.ModelSerializer):
#     user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
#     class Meta:
#         model = Review
#         fields = '__all__'
#         read_only_fields = ['user', 'is_approved', 'created_at']


# class ReviewCreateSerializer(serializers.ModelSerializer):
#     """Serializer for creating/updating reviews"""
    
#     class Meta:
#         model = Review
#         fields = ['business', 'rating', 'comment']
    
#     def validate_rating(self, value):
#         if not 1 <= value <= 5:
#             raise serializers.ValidationError("Rating must be between 1 and 5")
#         return value
    
#     def validate(self, attrs):
#         # منع المستخدم من تقييم محله الخاص
#         request = self.context.get('request')
#         if request and hasattr(attrs.get('business'), 'owner'):
#             if attrs['business'].owner == request.user:
#                 raise serializers.ValidationError("You cannot review your own business")
#         return attrs
