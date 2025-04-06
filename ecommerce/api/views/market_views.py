from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.market_dto import MarketDTO
from rest_framework.permissions import IsAuthenticated
from api.factories.service_factory import get_service_factory  # Import ServiceFactory
from api.permissions.permission_required_for_action import permission_required_for_action
from api.permissions.permissions import RoleRequiredPermission

class MarketViewSet(viewsets.ViewSet):

    required_roles = ['ADMIN', 'SUPPLIER']

    def get_permissions(self):
        # Apply permissions globally, but only to specific actions like 'list', 'update', etc.
        return [permission() for permission in self.permission_classes]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Get the service from the ServiceFactory
        service_factory = get_service_factory()
        self._service = service_factory.create_market_service(singleton=True)  # Get the singleton instance

    @permission_required_for_action({
        'list': [IsAuthenticated, RoleRequiredPermission],
    })
    def list(self, request):
        res = self._service.all()
        if res.status.succeeded:
            response_data = {
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': [{'id': market.id, 'name': market.name} for market in res.data]  # Format data as a list of dictionaries
            }
            return Response(response_data, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)


    @permission_required_for_action({
        'retrieve': [IsAuthenticated, RoleRequiredPermission],
    })
    def retrieve(self, request, pk=None):
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            response_data = {
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': res.data.to_dict()  # Return the market data in dictionary form
            }
            return Response(response_data, status=res.status.code)
        return Response({"error": res.status.message}, status=res.status.code)

    @permission_required_for_action({
        'create': [IsAuthenticated, RoleRequiredPermission],
    })
    def create(self, request):
        try:
            market_dto = MarketDTO(name=request.data.get('name'))
            result = self._service.add(market_dto)
            response_data = {
                'succeeded': result.status.succeeded,
                'message': result.status.message,
                'data': result.data.to_dict()  # Return the created market data
            }
            return Response(response_data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @permission_required_for_action({
        'update': [IsAuthenticated, RoleRequiredPermission],
    })
    def update(self, request, pk=None):
        try:
            market_dto = MarketDTO(id=pk, name=request.data.get('name'))
            result = self._service.update(market_dto)
            response_data = {
                'succeeded': result.status.succeeded,
                'message': result.status.message,
                'data': result.data.to_dict()  # Return the updated market data
            }
            return Response(response_data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @permission_required_for_action({
        'destroy': [IsAuthenticated, RoleRequiredPermission],
    })
    def destroy(self, request, pk=None):
        market_dto = MarketDTO(id=pk)
        res = self._service.delete(market_dto)
        if res:
            response_data = {
                'succeeded': True,
                'message': "Market deleted successfully",
                'data': {}
            }
            return Response(response_data, status=200)
        return Response({"error": "Market not found"}, status=404)
