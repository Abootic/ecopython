from typing import List

from django.forms import ValidationError
from api.services.interfaces.IuserService import IUserService
from api.repositories.interfaces.IuserRepository import IUserRepository
from api.dto.user_dto import UserDTO
from api.models.user import User

class UserService(IUserService):

  def __init__(self, user_repository: IUserRepository):
    self.user_repository = user_repository

  def all(self) -> List[UserDTO]:
        users = self.user_repository.all()
        return [UserDTO.from_model(u) for u in users]
  def get_user_by_id(self, user_id: int) -> UserDTO:
    return self.user_repository.get_by_id(user_id)

  def create_user(self, user_dto: UserDTO) -> UserDTO:
        # Create a User model instance from the DTO
        user_model = User(
            username=user_dto.username,
            user_type=user_dto.user_type,
            email=user_dto.email  # Include the email if needed
        )
        
        # Pass the user model to the repository's create method
        created_user = self.user_repository.create(user_model,user_dto.password)
        
        # Optionally convert the created user back to a DTO if needed
        return UserDTO.from_model(created_user)

  def update_user(self, user_dto: UserDTO) -> UserDTO:
    return self.user_repository.update(user_dto)

  def delete_user(self, user_id: int) -> bool:
    return self.user_repository.delete(user_id)
  def update_user_role(self, user_dto: UserDTO, new_role: str) -> UserDTO:
        # Assuming `new_role` is one of the choices: 'ADMIN', 'CUSTOMER', 'SUPPLIER'
        if new_role not in [User.ADMIN, User.CUSTOMER, User.SUPPLIER]:
            raise ValidationError("Invalid role")

        # Fetch the user from the repository
        user = self.user_repository.get_by_id(user_dto.id)
        if user is None:
            raise ValidationError("User not found")

        # Update the role
        user.user_type = new_role
        user.save()

        # Return the updated user as a DTO
        return UserDTO.from_model(user)
  def update_user_role(self, user_id: int, new_role: str) -> User:
        # Validate that the new role is a valid choice
        if new_role not in [User.UserRole.ADMIN, User.UserRole.CUSTOMER, User.UserRole.SUPPLIER]:
            raise ValidationError("Invalid role")

        # Call the repository to update the user's role
        data= self.user_repository.update_user_role(user_id, new_role)

        # Return the updated user as a DTO
        return UserDTO.from_model(data)