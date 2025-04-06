from api.repositories.interfaces.IproductRepository import IProductRepository
from api.services.interfaces.IproductService import IProductService
from api.dto.product_dto import ProductDTO
from api.models.product import Product
from typing import List
from api.wrpper.result import ConcreteResultT, ResultT
from api.Mapper.ProductMapper import ProductMapper


class ProductService(IProductService):

    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_by_id(self, product_id: int) -> ResultT:
        try:
            product = self.product_repository.get_by_id(product_id)
            if product:
                # Wrap the product data in a DTO and return success response
                product_dto = ProductDTO.from_model(product)
                return ConcreteResultT.success(product_dto)
            return ConcreteResultT.fail("Product not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving product: {str(e)}", 500)

    def all(self) -> ResultT:
        try:
            products = self.product_repository.all()  # Retrieve all products from the repository
            if products:
                product_dtos = ProductMapper.from_model_list(products)  # Convert Product models to ProductDTOs
                return ConcreteResultT.success(product_dtos)
            return ConcreteResultT.fail("No products found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving products: {str(e)}", 500)


    def add(self, product_dto: ProductDTO) -> ResultT:
        try:
            # Create a product instance from the DTO
            pro=ProductMapper.to_model(product_dto)
          
            added_product = self.product_repository.add(pro)
            # Return success with the added product DTO
            return ConcreteResultT.success("added successfully")
        except Exception as e:
            return ConcreteResultT.fail(f"Failed to add product: {str(e)}", 500)

    def update(self, product_dto: ProductDTO) -> ResultT:
        try:
            # Update the product instance from the DTO
            product = Product(
                id=product_dto.id,
                name=product_dto.name,
                price=product_dto.price,
                supplier_id=product_dto.supplier_id
            )
            updated_product = self.product_repository.update(product)
            # Return success with the updated product DTO
            return ConcreteResultT.success(ProductDTO.from_model(updated_product))
        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update product: {str(e)}", 500)

    def delete(self, product_dto: ProductDTO) -> ResultT:
        try:
            product = Product.objects.get(id=product_dto.id)
            if self.product_repository.delete(product):
                return ConcreteResultT.success("Product successfully deleted", 200)
            return ConcreteResultT.fail("Failed to delete product", 400)
        except Product.DoesNotExist:
            return ConcreteResultT.fail("Product not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)
