from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.contrib.auth import authenticate

class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        # Extract username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user (pass the request as the first argument)
        user = authenticate(request=request, username=username, password=password)

        # If authentication fails
        if user is None:
            return Response(
                {
                    'succeeded': False,
                    'message': 'Invalid credentials',
                    'data': None
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Prepare user data for the response
        user_data = {
            'id': user.id,  # Add the user ID
            'username': user.username if user.username else "",  # Ensure no null value
            'userType': user.user_type if user.user_type else "",  # Ensure no null value
        }

        # Return the response with the access token, refresh token, and user info
        return Response({
            'succeeded': True,
            'message': 'Login successful',
            'data': {
                'accessToken': access_token,
                'refreshToken': str(refresh),
                'user': user_data
            }
        }, status=status.HTTP_200_OK)
