from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.password_reset_serializer import PasswordResetSerializer
from ..serializers.password_reset_confirm_serializer import PasswordResetConfirmSerializer
from drf_spectacular.utils import extend_schema

class CustomPasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    @extend_schema(request=PasswordResetSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    @extend_schema(request=PasswordResetConfirmSerializer)
    def post(self, request, uidb64, token):
        data = request.data.copy()
        data['uid'] = uidb64
        data['token'] = token

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

