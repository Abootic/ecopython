from rest_framework import viewsets
from rest_framework.response import Response
from api.dto.percentage_dto import PercentageDTO
from api.services.interfaces.IPercentageService import IPercentageService
from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from injector import inject
from rest_framework import status

from api.factories.service_factory import get_service_factory  # Import your service factory

class PercentageViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN']

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize service using service_factory if not injected directly
        service_factory = get_service_factory()
        self._service = service_factory.create_percentage_service(singleton=True)

    @permission_required_for_action({'list': [IsAuthenticated, RoleRequiredPermission]})
    def list(self, request):
        """
        Retrieve a list of all percentages.
        """
        res = self._service.all()
        if res.status.succeeded:
            return Response({
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': [obj.__dict__ for obj in res.data]
            }, status=res.status.code)
        return Response({
            'succeeded': res.status.succeeded,
            'message': res.status.message,
            'data': []
        }, status=res.status.code)

    @permission_required_for_action({'retrieve': [IsAuthenticated, RoleRequiredPermission]})
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific percentage by ID.
        """
        res = self._service.get_by_id(pk)
        if res.status.succeeded:
            return Response({
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': res.data.to_dict()
            }, status=res.status.code)
        return Response({
            'succeeded': res.status.succeeded,
            'message': res.status.message,
            'data': {}
        }, status=res.status.code)

    @permission_required_for_action({'create': [IsAuthenticated, RoleRequiredPermission]})
    def create(self, request):
        """
        Create a new percentage entry.
        """
        try:
            percentage_dto = PercentageDTO(
                supplier_id=request.data.get('supplier_id'),
                market_id=request.data.get('market_id'),
                priority=request.data.get('priority'),
                percentage_value=request.data.get('percentage_value')
            )
            res = self._service.add(percentage_dto)
            return Response({
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': res.data or {}
            }, status=201 if res.status.succeeded else 400)

        except Exception as e:
            return Response({
                'succeeded': False,
                'message': str(e),
                'data': {}
            }, status=500)

    @permission_required_for_action({'update': [IsAuthenticated, RoleRequiredPermission]})
    def update(self, request, pk=None):
        """
        Update an existing percentage entry.
        """
        try:
            percentage_dto = PercentageDTO(
                id=pk,
                supplier_id=request.data.get('supplier_id'),
                market_id=request.data.get('market_id'),
                priority=request.data.get('priority'),
                percentage_value=request.data.get('percentage_value')
            )
            res = self._service.update(percentage_dto)
            return Response({
                'succeeded': res.status.succeeded,
                'message': res.status.message,
                'data': res.data or {}
            }, status=res.status.code)

        except Exception as e:
            return Response({
                'succeeded': False,
                'message': str(e),
                'data': {}
            }, status=500)

    @permission_required_for_action({'destroy': [IsAuthenticated, RoleRequiredPermission]})
    def destroy(self, request, pk=None):
        """
        Delete an existing percentage entry.
        """
        try:
            percentage_dto = PercentageDTO(id=pk)
            success = self._service.delete(percentage_dto)
            return Response({
                'succeeded': success.status.succeeded,
                'message': success.status.message,
                'data': {}
            }, status=204 if success.status.succeeded else 404)

        except Exception as e:
            return Response({
                'succeeded': False,
                'message': str(e),
                'data': {}
            }, status=500)

    @permission_required_for_action({'assign_percentage_value_to_suppliers': [IsAuthenticated, RoleRequiredPermission]})
    @action(detail=False, methods=['get'], url_path='assign_percentage_value_to_suppliers', url_name='assign_percentage_value_to_suppliers')

    def assign_percentage_value_to_suppliers(self, request, market_id=None):
       
        try:
            market_id = request.query_params.get('market_id')
            print(f"Received market_id: {market_id}")  # Log the received user_id

            if not market_id:
                return Response({
                    "succeeded": False,
                    "message": "User ID is required",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
            success = self._service.assign_percentage_value_to_suppliers(market_id)
            return Response({
                'succeeded': success.status.succeeded,
                'message': success.status.message,
                'data': {}
            }, status=204 if success.status.succeeded else 404)
        except Exception as e:
            return Response({
                'succeeded': False,
                'message': str(e),
                'data': {}
            }, status=500)
