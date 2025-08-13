# core/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from .models import User, Course, Offer, Purchase
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    CourseSerializer, OfferSerializer, PurchaseSerializer
)
from django.middleware.csrf import get_token


from django.contrib.auth import get_user_model
from django.http import JsonResponse

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)  # Django will create a session cookie
        return Response({
            "username": user.username,
            "role": "admin" if user.is_superuser else "user",
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff
        })
    else:
        return Response({"error": "Invalid credentials"}, status=401)



@api_view(['GET'])
def current_user(request):
    if request.user and request.user.is_authenticated:
        return Response(UserSerializer(request.user).data)
    return Response({})
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        # Exclude admin/superuser accounts
        return User.objects.filter(is_superuser=False, is_staff=False)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer

class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class OfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class PurchaseListView(generics.ListAPIView):
    queryset = Purchase.objects.all().order_by('-purchased_at')
    serializer_class = PurchaseSerializer


@csrf_exempt
@api_view(['POST'])
def checkout(request):
    course_ids = request.data.get('course_ids', [])
    if not course_ids:
        return Response({'error': 'No courses provided'}, status=status.HTTP_400_BAD_REQUEST)

    for course_id in course_ids:
        try:
            course = Course.objects.get(id=course_id)
            # Using anonymous purchases or dummy user
            Purchase.objects.create(user_id=1, course=course)  # change user_id=1 to a real user if needed
        except Course.DoesNotExist:
            return Response({'error': f'Course {course_id} not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'message': 'Purchase successful'}, status=status.HTTP_200_OK)





def reset_admin_password(request):
    User = get_user_model()
    try:
        admin = User.objects.get(username="admin")
        admin.set_password("newpassword123")
        admin.save()
        return JsonResponse({"status": "password updated"})
    except User.DoesNotExist:
        return JsonResponse({"error": "admin user not found"}, status=404)
