from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from api.dto.product_dto import ProductDTO
from api.factories.service_factory import get_service_factory
from api.permissions.permissions import RoleRequiredPermission
from api.services.interfaces.IproductService import IProductService
from rest_framework.permissions import IsAuthenticated
from api.permissions.permission_required_for_action import permission_required_for_action
from api.validation.validation_request import ValidationRequest

class ProductViewSet(viewsets.ViewSet):
    required_roles = ['ADMIN', 'SUPPLIER']
    def get_permissions(self):
       # No permissions required for 'create' action

        # Apply permissions globally, but only to specific actions like 'list', 'update', etc.
        return [permission() for permission in self.permission_classes]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        service_factory = get_service_factory()
        self.product_service = service_factory.create_product_service(singleton=True)
        self.supplier_service = service_factory.create_supplier_service(singleton=True)
        self.upload_service = service_factory.create_upload_file_service(singleton=True)

  
    @permission_required_for_action({'create': [IsAuthenticated, RoleRequiredPermission]})
    def create(self, request) -> Response:
            print(f"Received Data: {request.data}")
            try:
                # Define required fields
                required_fields = ['name', 'price', 'supplier_id', 'user_id']

                # Validate the main request data
                validation_error = ValidationRequest.validate_request_data(request.data, required_fields)
                if validation_error:
                    return validation_error

                # Handle base64 image, if provided
                image_path = None
                if 'image' in request.data and request.data['image']:
                    base64_string = request.data['image']
                    file_name = "uploaded_image.jpg"  # You can generate a dynamic name if needed
                    image_path = self.upload_service.upload_file_as_base64(base64_string, file_name, 'products')

                # Log image path to check if it is being set
               

                # Retrieve the supplier ID from the request or based on user_id
                supplier_id = request.data.get('supplier_id')

                # Check if supplier exists and get its ID
                supplier_result = self.supplier_service.get_supplier_by_userId(request.data.get('user_id'))
                if supplier_result.status.succeeded:
                    supplier_dto = supplier_result.data
                    supplier_id = supplier_dto.id
                else:
                    return Response({
                        'succeeded': False,
                        'message': supplier_result.status.message,
                        'data': {}
                    }, status=404)

                print(f"Supplier ID: {supplier_id}")

                # Create ProductDTO
                product_dto = ProductDTO(
                    name=request.data.get('name'),
                    price=request.data.get('price'),
                    supplier_id=supplier_id,
                    image=image_path,
                )

                # Log the product DTO
                print(f"Product DTO: {product_dto.to_dict()}")

                # Call the service to add the product
                res = self.product_service.add(product_dto)

                # Debugging: Check the type and content of res.data
                print(f"Response Data Type: {type(res.data)}")
                print(f"Response Data: {res.data}")

                # Prepare the response data
                response_data = {
                    "succeeded": res.status.succeeded,
                    "message": res.status.message,
                    "data": res.data.__dict__ if res.status.succeeded and hasattr(res.data, '__dict__') else str(res.data)
                }

                print("Product created successfully!" if res.status.succeeded else f"Product creation failed: {res.status.message}")
                return Response(response_data, status=201 if res.status.succeeded else 400)

            except Exception as e:
                print(f"Exception occurred: {str(e)}")
                return Response({"error": str(e)}, status=500)
            
    
    def list(self, request):
        try:
            res = self.product_service.all()
            if res.status.succeeded:
                response_data = {
                    "succeeded": res.status.succeeded,
                    "message": res.status.message,
                    "data": [obj.__dict__ for obj in res.data] if res.status.succeeded else []
                }
           # Add logging to print response data
                return Response(response_data, status=res.status.code)
            
            response_data = {
                "succeeded": res.status.succeeded,
                "message": res.status.message,
                "data": []
            }
             # Log the failed case as well
            return Response(response_data, status=res.status.code)
        except Exception as e:
           # Log any exceptions
            return Response({"error": str(e)}, status=500)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific product by ID.
        """
        res = self.product_service.get_by_id(pk)
        response_data = {
            "succeeded": res.status.succeeded,
            "message": res.status.message,
            "data": res.data.to_dict() if res.status.succeeded else {}
        }
        return Response(response_data, status=res.status.code)
    @permission_required_for_action({'update': [IsAuthenticated, RoleRequiredPermission]})
    def update(self, request, pk=None):
        """
        Update an existing product.
        """
        try:
            image = request.FILES.get('image')
            image_path = self.upload_service.upload_file_as_base64(image, 'products') if image else None

            product_dto = ProductDTO(
                id=pk,
                name=request.data.get('name'),
                price=request.data.get('price'),
                supplier_id=request.data.get('supplier_id'),
                image=image_path
            )

            res = self.product_service.update(product_dto)
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
        Delete a product.
        """
        try:
            product_dto = ProductDTO(id=pk)
            res = self.product_service.delete(product_dto)
            response_data = {
                "succeeded": res.status.succeeded,
                "message": "Product deleted successfully" if res.status.succeeded else res.status.message,
                "data": {}
            }
            return Response(response_data, status=204 if res.status.succeeded else res.status.code)
        except Exception as e:
            return Response({"succeeded": False, "message": str(e), "data": {}}, status=500)
