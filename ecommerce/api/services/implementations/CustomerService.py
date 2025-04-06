from api.Mapper.user_mapper import UserMapper
from api.dto.user_dto import UserDTO
from api.models.user import User
from api.repositories.interfaces.IcustomerRepository import ICustomerRepository
from api.repositories.interfaces.IuserRepository import IUserRepository
from api.services.interfaces.IcustomerService import ICustomerService
from api.dto.customer_dto import CustomerDTO
from api.models.customer import Customer
from typing import List
from api.Mapper.CustomerMapper import CustomerMapper
from api.wrpper.result import ConcreteResultT, ResultT
import random
import string
import json


class CustomerService(ICustomerService):
    def __init__(self, customer_repository:ICustomerRepository, user_repository:IUserRepository):  # Ensure the parameter name is userrepoaitory
        self.customer_repository = customer_repository
        self.user_repository = user_repository

    def get_by_id(self, Customer_id: int) -> ResultT:
        try:
            Customer = self.customer_repository.get_by_id(Customer_id)
            if Customer:
                Customer_dto = CustomerMapper.to_dto(Customer)
                return ConcreteResultT.success(Customer_dto)
            else:
                return ConcreteResultT.fail("Customer not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving Customer: {str(e)}", 500)

 

    def all(self) -> ResultT:
        try:
            customers = self.customer_repository.all()  # Get all customers
            users = self.user_repository.all()  # Get all users

            if not customers:
                return ConcreteResultT.fail("No customers found", 404)

            # Convert each customer to a DTO, including user details
            customer_dtos = []
            for customer in customers:
                user = next((u for u in users if u.id == customer.user_id), None)  # Find related user
                user_dto = UserMapper.to_dto(user) if user else None  # Convert user to DTO
                customer_dto = CustomerMapper.to_dto(customer, user_dto)  # Convert customer to DTO
                customer_dtos.append(customer_dto)

            # 

            return ConcreteResultT.success(customer_dtos)

        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving customers: {str(e)}", 500)

    def add(self, customer_dto: CustomerDTO) -> ResultT:
                try:
                    # Ensure user_dto is converted into UserDTO object if it's not already
                    user_dto = customer_dto.user_dto
                    if isinstance(user_dto, dict):
                        user_dto = UserDTO(**user_dto)  # Convert dict to UserDTO

                    # Generate supplier code
                    customer_dto.code = _generate_Customer_code()

                    # Check if supplier code already exists
                    if self.customer_repository.exists_by_code(customer_dto.code):
                        return ConcreteResultT.fail("Customer code already exists", 400)

                    # Create user model from the validated and mapped DTO
                    user_model = User(
                        username=user_dto.username,
                        user_type=user_dto.user_type,
                        email=user_dto.email,  # Include the email if needed,
                    )

                    # Create the user in the database using UserRepository
                    user = self.user_repository.create(user_model, user_dto.password)  # Make sure `create` exists here

                    # Create customer model (mapping from the DTO)
                    customer_model = Customer(
                        user=user,
                        code=customer_dto.code,
                    )

                    # Save the customer to the repository
                    customer = self.customer_repository.add(customer_model)

                    # Return success result with the created customer
                    return ConcreteResultT.success("Customer added successfully")

                except Exception as e:
                    return ConcreteResultT.fail(f"Failed to add customer: {str(e)}", 500)

    def update(self, customer_dto: CustomerDTO) -> ResultT:
        try:
            if not customer_dto.code:
                customer_dto.code = _generate_Customer_code()

            # Convert CustomerDTO to Customer model
            customer_model = CustomerMapper.to_model(customer_dto)

            # Check if user_dto is present and update the User
            if customer_dto.user_dto:
                user_dto = customer_dto.user_dto
                user_model = self.user_repository.get_by_id(customer_model.user_id)

                if user_model:
                    # Update the User with new values from user_dto (e.g., username)
                    user_model.username = user_dto.username if user_dto.username else user_model.username
                    user_model.email = user_dto.email if user_dto.email else user_model.email
                    user_model.user_type = user_dto.user_type if user_dto.user_type else user_model.user_type
                    
                    # Update the User in the repository
                    self.user_repository.update(user_model)

            # Update the Customer with the updated data
            updated_customer = self.customer_repository.update(customer_model)

            # Return success with updated Customer DTO
            return ConcreteResultT.success(CustomerMapper.to_dto(updated_customer))

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update Customer: {str(e)}", 500)


    def delete(self, entityDto: CustomerDTO) -> ResultT:
        try:
            # Use the repository to find and delete the Customer
            Customer = self.customer_repository.get_by_id(entityDto.id)
            if Customer:
                if self.customer_repository.delete(Customer):
                    return ConcreteResultT.success("Customer successfully deleted", 200)
                return ConcreteResultT.fail("Failed to delete Customer", 400)
            return ConcreteResultT.fail("Customer not found", 404)

        except Customer.DoesNotExist:
            return ConcreteResultT.fail("Customer not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)
    def get_supplier_by_code(self, code: str) -> CustomerDTO | None:
                try:
                    customer = self.customer_repository.get_by_code(code)
                    if customer:
                        customer_dto = CustomerMapper.to_dto(customer)
                        return ConcreteResultT.success(customer_dto)
                    else:
                        return ConcreteResultT.fail("customer not found", 404)
                except Exception as e:
                    return ConcreteResultT.fail(f"Error retrieving supplier: {str(e)}", 500)
    
   
    def get_customer_by_userId(self, userid: str) -> ResultT:
        try:
            # Fetch the supplier using the repository
            customer = self.customer_repository.get_by_userId(userid)
            if customer:
                # Fetch the related user from the supplier and convert to user_dto
                user_dto = UserDTO.from_model(customer.user) if customer.user else None

                # Convert supplier model to DTO using the mapper
                customer_dto = CustomerMapper.to_dto(customer, user_dto)
                
                return ConcreteResultT.success(customer_dto)

            else:
                return ConcreteResultT.fail("Supplier not found", 404)

        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving supplier: {str(e)}", 500)


def _generate_Customer_code() -> str:
    Customer_CODE_PREFIX = "SUP"
    Customer_CODE_LENGTH = 5
    Customer_CODE_TOTAL_LENGTH = 8
    random_code = ''.join(random.choices(string.digits, k=Customer_CODE_LENGTH))
    Customer_code = f"{Customer_CODE_PREFIX}{random_code}"
    
    if len(Customer_code) > Customer_CODE_TOTAL_LENGTH:
        raise ValueError(f"Generated Customer code exceeds the maximum length of {Customer_CODE_TOTAL_LENGTH} characters.")

    return Customer_code


