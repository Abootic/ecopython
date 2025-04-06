from rest_framework.permissions import BasePermission

class RoleRequiredPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the required role
        required_roles = getattr(view, 'required_roles', [])
        if not required_roles:
            return True  # If no role is required, allow the request

        user_role = request.user.user_type  # Assuming `user_type` field exists in your user model
        if user_role in required_roles:
            return True

        return False
