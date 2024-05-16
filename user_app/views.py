from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *


from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages







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






class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            # Check if the old password is correct
            if user.check_password(old_password):
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            # Change the password and save the user
            user.password = make_password(new_password)
            user.save()

            # Optionally, you may want to invalidate existing tokens
            Token.objects.filter(user=user).delete()

            return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
     
        
    
class UserList(APIView):
    def get(self, request):
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'User created successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        messages.error(request, 'Failed to create user.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = MyUserSerializer(user)
            return Response(serializer.data)
        messages.error(request, 'User not found.')
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = MyUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, 'User updated successfully.')
                return Response(serializer.data)
            messages.error(request, 'Failed to update user.')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        messages.error(request, 'User not found.')
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user:
            user.delete()
            messages.success(request, 'User deleted successfully.')
            return Response(status=status.HTTP_204_NO_CONTENT)
        messages.error(request, 'User not found.')
        return Response(status=status.HTTP_404_NOT_FOUND)    


    
    
    
    
# Create your views here.

def home(request):
    return render(request, 'home.html')




