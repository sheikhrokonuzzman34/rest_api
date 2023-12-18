from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, UserLoginSerializer


from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate






class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT refresh and access tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return success message along with tokens
            return Response({'message': 'User registered successfully', 'access_token': access_token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                return Response({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
#         try:
#             if not request.user.is_authenticated:
#                 raise NotFound(detail="User not found")

#             user = request.user
#             serializer = UserProfileSerializer(user, context={'request': request})
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except NotFound as e:
#             return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   


from rest_framework.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class UserPasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not user.check_password(current_password):
            raise ValidationError({'current_password': 'Current password is incorrect.'})

        form = PasswordChangeForm(user, {'new_password1': new_password, 'new_password2': confirm_password})
        if not form.is_valid():
            raise ValidationError(form.errors)

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)    
    
    
    



# Create your views here.

def home(request):
    return render(request, 'home.html')




