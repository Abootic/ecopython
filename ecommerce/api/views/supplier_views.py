from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from api.dto.Supplier_dto import SupplierDTO
from api.dto.user_dto import UserDTO
from api.services.interfaces.ISupplierService import ISupplierService
from api.permissions.permissions import RoleRequiredPermission
from api.factories.service_factory import get_service_factory
from api.permissions.permission_required_for_action import permission_required_for_action
from api.validation.validation_request import ValidationRequest


class SupplierViewSet(viewsets.GenericViewSet):
    required_roles = ['ADMIN', 'SUPPLIER']

    def get_permissions(self):
        """
        Handle permissions per action.
        """
        if self.action == 'create':
            return []  # No permissions required for 'create' action

        # Apply permissions globally, but only to specific actions like 'list', 'update', etc.
        return [permission() for permission in self.permission_classes]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        service_factory = get_service_factory()
        self._service = service_factory.create_supplier_service(singleton=True)

    @permission_required_for_action({
        'list': [IsAuthenticated, RoleRequiredPermission],
    })
    def list(self, request):
        """
        Retrieve all suppliers.
        """
        res = self._service.all()
        if res.status.succeeded:
            # Convert each SupplierDTO to a dictionary before returning
            data = [supplier.__dict__ for supplier in res.data]
            
            response_data = {
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': data  # Return the list of dictionaries
            }
            return Response(response_data, status=res.status.code)
        return Response({'succeeded': False, 'message': res.status.message}, status=res.status.code)


               

    @permission_required_for_action({
        'retrieve': [IsAuthenticated, RoleRequiredPermission],
    })
    def retrieve(self, request, pk=None):
        """
        Retrieve a single supplier by ID.
        """
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
             response_data = {
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': {'message': res.data}
            }
        return Response(response_data, status=res.status.code)

    def create(self, request):
        print(f"Received Data: {request.data}")
        try:
            # Define required fields
            required_fields = ['code', 'market_id', 'user_dto']  # Changed 'user' to 'user_dto'
            user_dto_required_fields = ['username', 'email', 'user_type', 'password']

            # Validate main request data
            validation_error = ValidationRequest.validate_request_data(request.data, required_fields)
            if validation_error:
                return validation_error

            # Validate 'user_dto' data (changed 'user' to 'user_dto')
            user_dto_data = request.data.get('user_dto')  # Access 'user_dto' instead of 'user'
            validation_error = ValidationRequest.validate_request_data(user_dto_data, user_dto_required_fields)
            if validation_error:
                return validation_error

            # Create UserDTO
            user_dto = UserDTO(**{field: user_dto_data[field] for field in user_dto_required_fields})

            # Create SupplierDTO
            supplier_dto = SupplierDTO(
                code=request.data['code'],
                market_id=request.data['market_id'],
                user_dto=user_dto
            )

            # Call the service to add the supplier
            result = self._service.add(supplier_dto)

            # Return response based on operation result
            response_data = {
                'succeeded': result.status.succeeded,
                'message': result.status.message,
                'data': {'message': result.data}
            }
            print("Supplier created successfully!" if result.status.succeeded else f"Supplier creation failed: {result.status.message}")
            return Response(response_data, status=200)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return Response({"error": str(e)}, status=500)

    @permission_required_for_action({
        'update': [IsAuthenticated, RoleRequiredPermission],
    })
    def update(self, request, pk=None):
        """
        Update an existing supplier.
        """
        try:
            data = request.data
            user_dto_data = data.get('user_dto')

            if user_dto_data:
                user_dto = UserDTO(**user_dto_data)
            else:
                return Response({"error": "User data is required"}, status=400)

            supplier_dto = SupplierDTO(
                id=data.get('id', pk),
                code=data.get('code'),
                user_dto=user_dto
            )

            result = self._service.update(supplier_dto)

            if result.status.succeeded:
                return Response(result.data.to_dict(), status=result.status.code)

            return Response({"error": result.status.message}, status=result.status.code)

        except Exception as e:
            return Response({"error": f"Error updating supplier: {str(e)}"}, status=500)

    @permission_required_for_action({
        'destroy': [IsAuthenticated, RoleRequiredPermission],
    })
    def destroy(self, request, pk=None):
        """
        Delete an existing supplier.
        """
        try:
            supplier_dto = SupplierDTO(id=pk)
            res = self._service.delete(supplier_dto)

            if res.status.succeeded:
                return Response({"message": "Supplier deleted successfully"}, status=204)
            return Response({"error": res.status.message}, status=res.status.code)

        except Exception as e:
            return Response({"error": f"Error deleting supplier: {str(e)}"}, status=500)

    @permission_required_for_action({
        'supplierCountInmarket': [IsAuthenticated, RoleRequiredPermission],
    })
    @action(detail=False, methods=['get'], url_path=r'supplierCountInmarket/(?P<marketid>\d+)')
    def supplierCountInmarket(self, request, marketid):
        """
        Get the supplier count by market ID.
        """
        res = self._service.count_by_market_id(marketid)
        if res.status.succeeded:
            return Response({"supplier_count": res.data}, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    @permission_required_for_action({
        'get_supplier_by_code': [IsAuthenticated, RoleRequiredPermission],
    })
    @action(detail=False, methods=['get'], url_path=r'get_supplier_by_code/(?P<code>[\w-]+)')
    def get_supplier_by_code(self, request, code):
        """
        Retrieve a supplier by code.
        """
        try:
            res = self._service.get_supplier_by_code(code)

            if res.status.succeeded:
                return Response({"supplier_code": res.data.to_dict()}, status=res.status.code)

            return Response({"error": res.status.message}, status=res.status.code)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)

    @permission_required_for_action({
        'get_supplier_by_UserId': [IsAuthenticated, RoleRequiredPermission],
    })

    @action(detail=False, methods=['get'], url_path=r'get_supplier_by_UserId/(?P<userid>[\d]+)')
    def get_supplier_by_UserId(self, request, userid):
        try:
            res = self._service.get_supplier_by_userId(userid)

            # Safely check if res.status.succeeded exists and is not None
            succeeded = res.status.succeeded if res.status.succeeded is not None else False
            print(f"succeeded: {succeeded}")

            if succeeded:
                # Directly return the supplier data in 'data' field
                data = res.data.__dict__ if res.data else {}

                return Response({
                    'succeeded': succeeded,
                    'message': res.status.message,
                    'data': data
                }, status=200)

            # If the status is not succeeded, return the failure response
            data = res.data.__dict__ if res.data else {}
            return Response({
                'succeeded': succeeded,
                'message': res.status.message,
                'data': data
            }, status=res.status.code)

        except Exception as e:
            # Return the exception response explicitly
            return Response({
                'succeeded': False,
                'message': f"An error occurred: {str(e)}",
                'data': {}
            }, status=500)


