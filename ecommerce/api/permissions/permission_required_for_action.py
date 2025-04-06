from functools import wraps
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.permissions.permissions import RoleRequiredPermission

def permission_required_for_action(actions_permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, request, *args, **kwargs):
            action = view.action
            permissions = actions_permissions.get(action, [])

            if permissions:
                view.permission_classes = permissions

                # Check if the user has permission
                for permission in permissions:
                    if not permission().has_permission(request, view):
                        return Response(
                            {"error": "You do not have permission to perform this action."}, 
                            status=status.HTTP_403_FORBIDDEN
                        )

            return view_func(view, request, *args, **kwargs)

        return _wrapped_view

    return decorator
