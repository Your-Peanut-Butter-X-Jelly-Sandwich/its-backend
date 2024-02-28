from django.db import IntegrityError
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework import status
from rest_framework import serializers
from .serializers import SignUpSerializer, SignInSerializer, SocialCallbackSerializer, RetrieveUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = SignUpSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except IntegrityError as e:
            return Response(data={"message": e.args}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = [AllowAny,]
    serializer_class = SignInSerializer
    
    def get(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.get(email=serializer.data['email'])
            tokens = generate_tokens_for_user(user)
            print(serializer.data)
            return Response(data={
                "tokens": tokens,
                "user": serializer.data
                }, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        refresh_token = request.data['tokens']['refresh_token']
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refersh_token = RefreshToken(refresh_token)
            refersh_token.blacklist()
            logout(request)
            return Response({'message': 'User successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = ['http', 'https']

class SocialCallbackView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = SocialCallbackSerializer
    def get(self, request):
        user = request.user
        tokens = generate_tokens_for_user(user)
        redirect_url = f'http://localhost:3000/en/auth/post-social-auth?access={tokens["access"]}&refresh={tokens["refresh"]}'
        return CustomRedirect(redirect_url)
        
class RetrieveUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RetrieveUserSerializer
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(instance=user)
        try:
            return Response(data={
                "user": serializer.data,
            }, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(views.APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        '''
        Example request:
        {
            "old_password": "sampleOldPassword123",
            "new_password": "sampleNewPassword456"
        }
        '''

        # Get current user and payload data
        user: CustomUser = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Check if old_password and new_password are provided in request data
        if not old_password or not new_password:
            return Response({'error': 'Old password and new password are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verify old password
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
