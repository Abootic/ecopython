from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.factories.service_factory import get_service_factory
from api.services.interfaces.IuserService import IUserService
from api.dto.user_dto import UserDTO
from api.permissions.permissions import RoleRequiredPermission
from rest_framework.decorators import action
from injector import inject


class UserViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN']  # Define required roles for this view

    def get_permissions(self):
        """
        Dynamically apply permissions based on action.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, RoleRequiredPermission]
        else:
            permission_classes = [IsAuthenticated, RoleRequiredPermission]
        return [permission() for permission in permission_classes]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use ServiceFactory to get the service instance
        service_factory = get_service_factory()  # Singleton instance of ServiceFactory
        self.user_service = service_factory.create_user_service(singleton=True)  # Get the service

    def list(self, request):
        # List all users
        try:
            users = self.user_service.all()
            return Response([user.to_dict() for user in users])
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        # Retrieve user by ID
        try:
            user_dto = self.user_service.get_user_by_id(pk)
            if user_dto:
                return Response(user_dto.to_dict())
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        # Create a new user
        try:
            user_dto = UserDTO(
                username=request.data.get('username'),
                user_type=request.data.get('user_type'),
                email=request.data.get('email'),
                password=request.data.get('password')
            )
            created_user = self.user_service.create_user(user_dto)
            return Response(created_user.to_dict(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        # Update user information
        try:
            user_dto = UserDTO(
                id=pk,
                username=request.data.get('username'),
                user_type=request.data.get('user_type'),
                email=request.data.get('email'),
                password=request.data.get('password')
            )
            updated_user = self.user_service.update_user(user_dto)
            if updated_user:
                return Response(updated_user.to_dict())
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        # Delete user
        try:
            success = self.user_service.delete_user(pk)
            if success:
                return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['put'], url_path='update-role')
    def update_role(self, request, pk=None):
        """
        Custom action to update the user's role (user_type).
        """
        new_role = request.data.get('user_type')
        
        # Validate role
        if not new_role:
            return Response({"error": "Role is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        allowed_roles = ['ADMIN', 'CUSTOMER', 'SUPPLIER']  # Adjust the allowed roles as per your needs
        if new_role not in allowed_roles:
            return Response({"error": f"Invalid role. Allowed roles are: {', '.join(allowed_roles)}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_user = self.user_service.update_user_role(pk, new_role)
            return Response({"message": f"User role updated to {updated_user.user_type}"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
