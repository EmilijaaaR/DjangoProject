from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.serializers import RegisterSerializer, LoginSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminUser
from rest_framework.generics import UpdateAPIView
from users.serializers.user_update_serializer import UserUpdateSerializer
from users.serializers.serializers import UserDeactivateSerializer

class RegisterView(APIView):
    @extend_schema(request=RegisterSerializer, responses={201: None})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @extend_schema(request=LoginSerializer, responses={200: None})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "email": user.email,
                }
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class SomeAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "Samo admin ima pristup."})

class UserProfileUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDeactivateSerializer

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "Account deactivated."})