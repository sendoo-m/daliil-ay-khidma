# apps/api/views/auth.py

"""Authentication API Views"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from apps.directory.models import Business


User = get_user_model()


# ══════════════════════════════════════════
# Helper
# ══════════════════════════════════════════
def get_user_role(user):
    """تحديد دور المستخدم للـ Flutter"""
    if user.is_superuser or user.is_staff:
        return 'admin'
    if user.is_business_owner or Business.objects.filter(owner=user).exists():
        return 'business_owner'
    return 'user'


def build_user_data(user):
    """بيانات المستخدم الكاملة"""
    return {
        'id':               user.id,
        'username':         user.username,
        'email':            user.email,
        'first_name':       user.first_name,
        'last_name':        user.last_name,
        'phone':            getattr(user, 'phone', ''),
        'profile_picture':  user.get_profile_picture_url() if hasattr(user, 'get_profile_picture_url') else None,
        'bio':              getattr(user, 'bio', ''),
        'city':             getattr(user, 'city', ''),
        'role':             get_user_role(user),
        'is_staff':         user.is_staff,
        'is_superuser':     user.is_superuser,
        'is_business_owner': getattr(user, 'is_business_owner', False),
        'is_active':        user.is_active,
        'email_verified':   getattr(user, 'email_verified', False),
        'date_joined':      user.date_joined,
        'last_login':       user.last_login,
    }


# ══════════════════════════════════════════
# JWT Custom Serializer
# ══════════════════════════════════════════
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer with user info"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims داخل الـ token
        token['username']         = user.username
        token['email']            = user.email
        token['role']             = get_user_role(user)
        token['is_staff']         = user.is_staff
        token['is_superuser']     = user.is_superuser
        token['is_business_owner'] = getattr(user, 'is_business_owner', False)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # أضف بيانات المستخدم مع الـ tokens في الـ response
        data['user'] = build_user_data(self.user)
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view"""
    serializer_class = CustomTokenObtainPairSerializer


# ══════════════════════════════════════════
# REGISTER
# ══════════════════════════════════════════
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register new user"""
    username         = request.data.get('username', '').strip()
    email            = request.data.get('email', '').strip()
    password         = request.data.get('password', '').strip()
    password_confirm = request.data.get('password_confirm', '').strip()
    first_name       = request.data.get('first_name', '').strip()
    last_name        = request.data.get('last_name', '').strip()
    phone            = request.data.get('phone', '').strip()

    # Validation
    if not all([username, email, password, password_confirm]):
        return Response(
            {'error': 'username و email و password و password_confirm مطلوبين'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if password != password_confirm:
        return Response(
            {'error': 'كلمتا المرور غير متطابقتين'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'اسم المستخدم موجود بالفعل'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'البريد الإلكتروني مسجل بالفعل'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if phone and User.objects.filter(phone=phone).exists():
        return Response(
            {'error': 'رقم الهاتف مسجل بالفعل'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_password(password)
    except ValidationError as e:
        return Response(
            {'error': list(e.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        create_kwargs = dict(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        if phone:
            create_kwargs['phone'] = phone

        user = User.objects.create_user(**create_kwargs)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'تم إنشاء الحساب بنجاح',
        'user':    build_user_data(user),
        'tokens': {
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
        }
    }, status=status.HTTP_201_CREATED)


# ══════════════════════════════════════════
# PROFILE
# ══════════════════════════════════════════
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    return Response(build_user_data(request.user))


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """Update current user profile"""
    user    = request.user
    allowed = ['first_name', 'last_name', 'email', 'phone', 'bio', 'city']

    for field in allowed:
        if field in request.data:
            setattr(user, field, request.data[field])

    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']

    try:
        user.save()
        return Response({
            'message': 'تم تحديث الملف الشخصي بنجاح',
            'user':    build_user_data(user),
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ══════════════════════════════════════════
# CHANGE PASSWORD
# ══════════════════════════════════════════
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    user                 = request.user
    old_password         = request.data.get('old_password', '')
    new_password         = request.data.get('new_password', '')
    new_password_confirm = request.data.get('new_password_confirm', '')

    if not all([old_password, new_password, new_password_confirm]):
        return Response(
            {'error': 'جميع الحقول مطلوبة'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not user.check_password(old_password):
        return Response(
            {'error': 'كلمة المرور الحالية غير صحيحة'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != new_password_confirm:
        return Response(
            {'error': 'كلمتا المرور الجديدتان غير متطابقتين'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_password(new_password, user)
    except ValidationError as e:
        return Response(
            {'error': list(e.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.save()

    # أنشئ tokens جديدة بعد تغيير كلمة المرور
    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'تم تغيير كلمة المرور بنجاح',
        'tokens': {
            'refresh': str(refresh),
            'access':  str(refresh.access_token),
        }
    })
