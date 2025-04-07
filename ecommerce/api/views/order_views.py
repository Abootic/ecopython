from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.dto.order_dto import OrderDTO

from rest_framework.decorators import action
from api.factories.service_factory import ServiceFactory
from api.permissions.permissions import RoleRequiredPermission
from api.permissions.permission_required_for_action import permission_required_for_action
from api.validation.validation_request import ValidationRequest
from rest_framework.permissions import IsAuthenticated

from api.models.supplierProfit import SupplierProfit
from api.models.percentage import Percentage


class OrderViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'CUSTOMER','SUPLLIER']
    
    def get_permissions(self):
       
        return [permission() for permission in self.permission_classes]

    def __init__(self, *args, **kwargs):
        """
        Initialize the OrderViewSet with the OrderService created by ServiceFactory.
        """
        service_factory = ServiceFactory()  # Create an instance of ServiceFactory
        self.order_service = service_factory.create_order_service(singleton=True)  # Use the factory to get the service
        self.customer_service = service_factory.create_customer_service(singleton=True)  
        self.supplier_service = service_factory.create_supplier_service(singleton=True)  
        
        super().__init__(*args, **kwargs)

    def list(self, request):
        """
        Retrieve a list of all orders.
        """
        res = self.order_service.all()
        response_data = {
            "succeeded": res.status.succeeded,
            "message": res.status.message,
            "data": [obj.__dict__ for obj in res.data] if res.status.succeeded else []
        }
        return Response(response_data, status=res.status.code)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific order by ID.
        """
        res = self.order_service.get_by_id(pk)
        response_data = {
            "succeeded": res.status.succeeded,
            "message": res.status.message,
            "data": res.data.to_dict() if res.status.succeeded else {}
        }
        return Response(response_data, status=res.status.code)

    @permission_required_for_action({'create': [IsAuthenticated, RoleRequiredPermission]})
    def create(self, request):
        """
        Create a new order.
        """
        try:
            required_fields = ['product_id', 'quantity', 'user_id']

            # Validate the request data
            validation_error = ValidationRequest.validate_request_data(request.data, required_fields)
            if validation_error:
                print(f"Validation Error: {validation_error}")  # Log the validation error
                return validation_error

            print(f"Coming from Flutter: {request.data}")

            # Retrieve the customer ID from the user_id
            customer_id = 0

            customer_result = self.customer_service.get_customer_by_userId(request.data.get('user_id'))
            print(f"Customer result: {customer_result.status.succeeded}, id: {customer_result.data.id}")

            if customer_result.status.succeeded:
                customer_dto = customer_result.data
                customer_id = customer_dto.id
            else:
                return Response({
                    'succeeded': False,
                    'message': customer_result.status.message,
                    'data': {}
                }, status=404)

            print(f"Customer ID: {customer_id}")

            # Create OrderDTO
            order_dto = OrderDTO(
                product_id=int(request.data.get('product_id')),  # Ensure product_id is an integer
                quantity=int(request.data.get('quantity')),  # Ensure quantity is an integer
                customer_id=customer_id,  # Ensure user_id is an integer
                price=float(request.data.get('price')),
                total_price=0  # Ensure price is a float
            )

            # Call the service to add the order
            res = self.order_service.add(order_dto)

            print(f"Order Service Response: {res.status.succeeded}, Message: {res.status.message}")

            response_data = {
                "succeeded": res.status.succeeded,
                "message": res.status.message,
                "data": res.data.__dict__ if res.status.succeeded and hasattr(res.data, '__dict__') else str(res.data)
            }

            return Response(response_data, status=201 if res.status.succeeded else 400)

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @permission_required_for_action({'update': [IsAuthenticated, RoleRequiredPermission]})
    def update(self, request, pk=None):
        """
        Update an existing order.
        """
        try:
            order_data = request.data
            order_dto = OrderDTO(**order_data)
            order_dto.id = pk
            res = self.order_service.update(order_dto)

            response_data = {
                "succeeded": res.status.succeeded,
                "message": res.status.message,
                "data": res.data.to_dict() if res.status.succeeded else {}
            }

            return Response(response_data, status=res.status.code)
        except Exception as e:
            return Response({"succeeded": False, "message": str(e), "data": {}}, status=500)

    @permission_required_for_action({'destroy': [IsAuthenticated, RoleRequiredPermission]})
    def destroy(self, request, pk=None):
        """
        Delete an existing order.
        """
        try:
            res = self.order_service.get_by_id(pk)
            if res.status.succeeded:
                order = res.data
                delete_result = self.order_service.delete(order)
                response_data = {
                    "succeeded": delete_result.status.succeeded,
                    "message": delete_result.status.message,
                    "data": {}
                }
                return Response(response_data, status=204 if delete_result.status.succeeded else 400)
            return Response({"error": res.status.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @permission_required_for_action({'get_customer_order': [IsAuthenticated, RoleRequiredPermission]})
    @action(detail=False, methods=['get'], url_path='get_customer_order', url_name='get-customer-order')
    def get_customer_order(self, request):
        
        try:
            print("coming from flutter ")
            # Retrieve 'user_id' from the query parameters (GET request)
            user_id = request.query_params.get('user_id')
            print(f"Received user_id: {user_id}")  # Log the received user_id

            if not user_id:
                return Response({
                    "succeeded": False,
                    "message": "User ID is required",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
            customer_id = 0

            customer_result = self.customer_service.get_customer_by_userId(user_id)
            print(f"Customer result: {customer_result.status.succeeded}, id: {customer_result.data.id}")

            if customer_result.status.succeeded:
                customer_dto = customer_result.data
                customer_id = customer_dto.id
            else:
                return Response({
                    'succeeded': False,
                    'message': customer_result.status.message,
                    'data': {}
                }, status=404)

            print(f"Customer ID: {customer_id}")
            # Call the service to get orders for the customer
            res = self.order_service.get_orders_by_customer(customer_id)
            print(f"message for get_customer_order is {res.status.message}")
            response_data = {
                "succeeded": res.status.succeeded,
                "message": res.status.message,
                "data": [order.to_dict() for order in res.data] if res.status.succeeded else []
            }
            return Response(response_data, status=res.status.code)

        except Exception as e:
            print(f"Exception: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], url_path='calculate-profit/user_id/(?P<user_id>\d+)', url_name='calculate-profit')
    def calculate_profit(self, request,user_id=None):  # pk is the id of the object in the viewset
       
        print(f"=================================================================")  # Log the received user_id
        print(f"Received user_id: {user_id}")  # Log the received user_id
        print(f"====================================================================")  # Log the received user_id


        if not user_id:
            return Response({
                "succeeded": False,
                "message": "User ID is required",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve supplier information based on the user_id
        supplierRes = self.supplier_service.get_supplier_by_userId(user_id)

        # Check if the supplier retrieval was successful
        if supplierRes.status.succeeded:
            print(f"=================================================================")  # Log the received user_id
            print(f"Received supplier: {supplierRes.data.id}")  # Log the received user_id
            print(f"====================================================================")  # Log the received user_id
            supplierid = supplierRes.data.id  # If succeeded, extract supplier ID
        else:
            supplierid = 0  # If not succeeded, set supplierid to 0
        
        # Calculate the supplier profit
        res = self.order_service.calculate_supplier_profit(supplierid)

        # Construct the response data
        response_data = {
            "succeeded": res.status.succeeded,
            "message": res.status.message,
            "data": res.data if res.status.succeeded else {}
        }
        
        return Response(response_data, status=res.status.code)

    def process_order(self, request, pk=None):
        """
        Process an order, including calculating profit and updating the supplier.
        """
        res = self.order_service.process_order(pk)
        response_data = {
            "succeeded": res.status.succeeded,
            "message": res.status.message,
            "data": res.data if res.status.succeeded else {}
        }
        return Response(response_data, status=res.status.code)
        

    @action(detail=False, methods=['post'], url_path='get_supplier_profit', url_name='get_supplier_profit')
    def get_supplier_profit(self, request):
        try:
            # Log Request Data
            print("==================================   Request Data ===============================================")
            print(f"Request data type: {type(request.data)}")
            print(f"Request data: {request.data}")
            print("=========================================================================================")

            # Validate request data for required fields
            required_fields = ['user_id']
            validation_error = self.validate_request_data(request.data, required_fields)
            if validation_error:
                return validation_error  # Return directly if validation fails

            user_id = request.data.get('user_id')
            print(f"Extracted user_id: {user_id}")

            # Get Supplier Data using Supplier Service
            supplierRes = self.supplier_service.get_supplier_by_userId(user_id)
            print("==================================   Supplier Service Response ===============================================")
            print(f"Supplier response status: {supplierRes.status.succeeded}")
            print(f"Supplier response data type: {type(supplierRes.data)}")
            print(f"Supplier response data: {supplierRes.data}")
            print("=========================================================================================")

            if not supplierRes.status.succeeded:
                print("Supplier not found, returning 404")
                return Response({
                    "succeeded": False,
                    "message": "Supplier not found",
                    "data": {}
                }, status=status.HTTP_404_NOT_FOUND)

            supplier_data = supplierRes.data  # SupplierDTO object
            supplier_id = supplier_data.id
            print(f"Supplier ID from SupplierDTO: {supplier_id}")

            # Querying SupplierProfit data
            print(f"Querying SupplierProfit for supplier_id={supplier_id}")
            profit_record = SupplierProfit.objects.filter(supplier_id=supplier_id).order_by('-id').first()
            profit_data = self.format_profit_data(profit_record, supplier_id)

            # Querying Percentage data for the supplier (now returning the first record or null if not found)
            percentage_record = Percentage.objects.filter(supplier_id=supplier_id).order_by('priority').first()

            # Check if percentage_record exists and format it
            if percentage_record:
                percentage_data = {
                    "market_id": percentage_record.market.id,
                    "market_name": percentage_record.market.name,  # Assuming 'name' exists in the Market model
                    "percentage_value": percentage_record.percentage_value,
                    "priority": percentage_record.priority
                }
            else:
                percentage_data = None  # If no percentage data is found, set it to None

            # Construct final response with Supplier, Profit, and Percentage data
            obj = self.construct_response(supplier_data, profit_data, percentage_data)

            # Log Final Response
            print("==================================   Final Response Data ===============================================")
            print(f"Response object: {obj}")
            print("=========================================================================================")

            return Response(obj, status=status.HTTP_200_OK)

        except Exception as e:
            print("==================================   Exception Caught ===============================================")
            print(f"Error in get_supplier_profit: {str(e)}")
            print(f"Exception type: {type(e)}")
            print("=========================================================================================")
            return Response({
                "succeeded": False,
                "message": f"Internal Server Error: {str(e)}",
                "data": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def validate_request_data(self, data, required_fields):
        for field in required_fields:
            if field not in data:
                return Response({
                    "succeeded": False,
                    "message": f"Missing field: {field}",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)
        return None

    def format_profit_data(self, profit_record, supplier_id):
        if profit_record:
            return {
                "id": profit_record.id,
                "supplier_id": profit_record.supplier_id,
                "profit": float(profit_record.profit),
                "month": profit_record.month.isoformat() if profit_record.month else None,
            }
        return {
            "id": None,
            "supplier_id": supplier_id,
            "profit": 0.0,
            "month": timezone.now().date().isoformat(),
        }

    def construct_response(self, supplier_data, profit_data, percentage_data):
        return {
            "succeeded": True,
            "message": "Data retrieved successfully",
            "data": {
                "supplier": {
                    "id": supplier_data.id,
                    "user_id": supplier_data.user_id,
                    "market_id": supplier_data.market_id,
                    "code": supplier_data.code,
                    "user_dto": {
                        "id": supplier_data.user_dto.get('id'),
                        "username": supplier_data.user_dto.get('username'),
                        "email": supplier_data.user_dto.get('email'),
                    },
                    "join_date": supplier_data.join_date.isoformat() if supplier_data.join_date else None
                },
                "profit_data": profit_data,
                "percentage_data": percentage_data  # Return single Percentage object or None
            }
        }