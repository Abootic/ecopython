from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.factories.service_factory import get_service_factory
from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
from api.services.interfaces.ISupplierProfitService import ISupplierProfitService

from api.validation.validation_request import ValidationRequest


class SupplierProfitViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN']  # Define roles allowed for this view

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use ServiceFactory to get the service instance
        service_factory = get_service_factory()  # Singleton instance of ServiceFactory
        self._service = service_factory.create_supplier_profit_service(singleton=True)  # Get the service

    @permission_required_for_action({
        'create': [IsAuthenticated, RoleRequiredPermission],
        'list': [IsAuthenticated, RoleRequiredPermission],
    })
 
    
    def create(self, request):
        """
        Create or update the supplier profit for a given market and month.
        """
        print(f"Received Data: {request.data}")
        try:
            # Define required fields for the request data
            required_fields = ['market_id', 'month']

            # Validate main request data
            validation_error = ValidationRequest.validate_request_data(request.data, required_fields)
            if validation_error:
                return validation_error

            # Validate market_id and month individually if needed
            market_id = request.data.get('market_id')
            month = request.data.get('month')

            if not market_id or not month:
                return Response({"error": "Market ID and month are required."}, status=status.HTTP_400_BAD_REQUEST)

            # If the month is in YYYY-MM format, append "-01" to make it a full date
            if len(month) == 7:  # Assuming it's in YYYY-MM format
                month = f"{month}-01"  # Change to YYYY-MM-DD

            # Now, attempt to parse the month to a valid date
            try:
                parsed_date = datetime.strptime(month, "%Y-%m-%d")
            except ValueError:
                return Response({"error": f"Invalid date format: {month}. It must be in YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)

            # Call the service to update or create the profit
            result = self._service.update_or_create_profit(market_id, month)

            # Create the response data based on the result
            response_data = {
                'succeeded': result.status.succeeded,
                'message': result.status.message,
                'data': { result.data}
            }

            # Return response based on operation result
            if result.status.succeeded:
                print("Supplier profit updated successfully!")
                return Response(response_data, status=status.HTTP_200_OK)
            
            print(f"Supplier profit update failed: {result.status.message}")
            return Response(response_data, status=result.status.code)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
            """
            List all supplier profits.
            """
            try:
                res = self._service.all()
                if res.status.succeeded:
                    return Response([obj.to_dict() for obj in res.data], status=res.status.code)
                return Response({"error": res.status.message}, status=res.status.code)
            except Exception as e:
                return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)