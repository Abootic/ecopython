from api.Mapper.user_mapper import UserMapper
from api.dto.user_dto import UserDTO
from api.models.user import User
from api.repositories.interfaces.IsupplierRepository import ISupplierRepository
from api.repositories.interfaces.IuserRepository import IUserRepository
from api.services.interfaces.ISupplierService import ISupplierService
from api.dto.Supplier_dto import SupplierDTO
from api.models.supplier import Supplier
from typing import List
from api.Mapper.SupplierMapper import SupplierMapper
from api.wrpper.result import ConcreteResultT, ResultT
import random
import string
import json


class SupplierService(ISupplierService):
    def __init__(self, supplier_repository: ISupplierRepository, user_repository: IUserRepository):
        self.supplier_repository = supplier_repository
        self.user_repository = user_repository

    def get_by_id(self, supplier_id: int) -> ResultT:
        try:
            supplier = self.supplier_repository.get_by_id(supplier_id)
            if supplier:
                supplier_dto = SupplierMapper.to_dto(supplier)
                return ConcreteResultT.success(supplier_dto)
            else:
                return ConcreteResultT.fail("Supplier not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving supplier: {str(e)}", 500)

    def all(self) -> List[SupplierDTO]:
        try:
            suppliers = self.supplier_repository.all()
            supplier_dtos = []

            for supplier in suppliers:
                user = supplier.user
                user_dto = UserMapper.to_dto(user) if user else None
                supplier_dto = SupplierMapper.to_dto(supplier, user_dto)
                supplier_dtos.append(supplier_dto)

            return ConcreteResultT.success(supplier_dtos)
        except Exception as e:
            return ConcreteResultT.fail(f"Failed to retrieve suppliers: {str(e)}", 500)

    def _generate_supplier_code(self) -> str:
        SUPPLIER_CODE_PREFIX = "SUP"
        SUPPLIER_CODE_LENGTH = 5
        SUPPLIER_CODE_TOTAL_LENGTH = 8

        random_code = ''.join(random.choices(string.digits, k=SUPPLIER_CODE_LENGTH))
        supplier_code = f"{SUPPLIER_CODE_PREFIX}{random_code}"

        if len(supplier_code) != SUPPLIER_CODE_TOTAL_LENGTH:
            raise ValueError(f"Generated supplier code must have {SUPPLIER_CODE_TOTAL_LENGTH} characters.")
        
        return supplier_code

    def add(self, supplier_dto: SupplierDTO) -> ResultT:
        try:
            if isinstance(supplier_dto.code, tuple):
                supplier_dto.code = supplier_dto.code[0]

            json_str = json.dumps(supplier_dto.to_dict(), default=str)

            user_dto = supplier_dto.user_dto
            if not user_dto:
                return ConcreteResultT.fail("User DTO is None", 400)

            if isinstance(user_dto, dict):
                user_dto = UserDTO(**user_dto)

            if not user_dto.username or not user_dto.email:
                return ConcreteResultT.fail("User DTO missing required fields", 400)

            supplier_dto.code = self._generate_supplier_code()

            if self.supplier_repository.exists_by_code(supplier_dto.code):
                return ConcreteResultT.fail("Supplier code already exists", 400)

            existing_supplier_count = self.supplier_repository.count_by_market_id(supplier_dto.market_id)
            if existing_supplier_count >= 10:
                return ConcreteResultT.fail("Market already has the maximum number of suppliers (10)", 400)

            user_model = User(
                username=user_dto.username,
                user_type=user_dto.user_type,
                email=user_dto.email,
            )

            user = self.user_repository.create(user_model, user_dto.password)
            if not user:
                return ConcreteResultT.fail("Failed to create user", 500)

            supplier_model = Supplier(
                user=user,
                code=supplier_dto.code,
                market_id=supplier_dto.market_id
            )

            supplier = self.supplier_repository.add(supplier_model)
            if supplier:
                return ConcreteResultT.success("Supplier added successfully")
            return ConcreteResultT.fail("Failed to create Supplier", 500)
        except Exception as e:
            return ConcreteResultT.fail(f"Failed to add supplier: {str(e)}", 500)

    def update(self, supplier_dto: SupplierDTO) -> ResultT:
        try:
            supplier = self.supplier_repository.get_by_id(supplier_dto.id)
            if not supplier:
                return ConcreteResultT.fail("Supplier not found", 404)

            if supplier_dto.user_dto:
                user_model = self.user_repository.get_by_id(supplier_dto.user_id)
                if user_model:
                    user_model.username = supplier_dto.user_dto.username
                    user_model.email = supplier_dto.user_dto.email
                    user_model.user_type = supplier_dto.user_dto.user_type
                    self.user_repository.update(user_model)
                else:
                    return ConcreteResultT.fail("User not found", 404)

            supplier.code = supplier_dto.code or supplier.code
            if isinstance(supplier.code, tuple):
                supplier.code = supplier.code[0]

            self.supplier_repository.update(supplier)

            updated_supplier_dto = SupplierMapper.to_dto(supplier)
            return ConcreteResultT.success(updated_supplier_dto)

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update supplier: {str(e)}", 500)

    def delete(self, entityDto: SupplierDTO) -> ResultT:
        try:
            supplier = self.supplier_repository.get_by_id(entityDto.id)
            if supplier:
                if self.supplier_repository.delete(supplier):
                    return ConcreteResultT.success({"message": "Supplier successfully deleted", "status_code": 200})
                return ConcreteResultT.fail("Failed to delete supplier", 400)
            return ConcreteResultT.fail("Supplier not found", 404)
        except Supplier.DoesNotExist:
            return ConcreteResultT.fail("Supplier not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)

    def count_by_market_id(self, marketid) -> ResultT:
        try:
            supplier_count = self.supplier_repository.count_by_market_id(marketid)
            if supplier_count is not None:
                return ConcreteResultT.success(supplier_count)
            else:
                return ConcreteResultT.fail("No suppliers found in this market", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving suppliers: {str(e)}", 500)

    def get_supplier_by_code(self, code: str) -> ResultT:
        try:
            supplier = self.supplier_repository.get_by_code(code)
            if supplier:
                supplier_dto = SupplierMapper.to_dto(supplier)
                return ConcreteResultT.success(supplier_dto)
            else:
                return ConcreteResultT.fail("Supplier not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving supplier: {str(e)}", 500)
   
    def get_supplier_by_userId(self, userid: str) -> ResultT:
        try:
            # Fetch the supplier using the repository
            supplier = self.supplier_repository.get_by_userId(userid)
            if supplier:
                # Fetch the related user from the supplier and convert to user_dto
                user_dto = UserDTO.from_model(supplier.user) if supplier.user else None

                # Convert supplier model to DTO using the mapper
                supplier_dto = SupplierMapper.to_dto(supplier, user_dto)
                
                return ConcreteResultT.success(supplier_dto)

            else:
                return ConcreteResultT.fail("Supplier not found", 404)

        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving supplier: {str(e)}", 500)


