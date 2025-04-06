import logging
from typing import List
from api.models.user import User
from django.core.exceptions import ValidationError # type: ignore
from api.repositories.interfaces.IuserRepository import IUserRepository

class UserRepository(IUserRepository):
  def all(self) -> List[User]:
    return User.objects.all()
  def get_by_id(self, user_id: int) -> User:
    try:
      user = User.objects.get(id=user_id)
      return user
    except User.DoesNotExist:
      logging.error(f"User with id {user_id} does not exist.")
      return None

  def create(self, user: User,password) -> User:
        # Trim password to remove any leading or trailing spaces
      password =password

        # Check if password length is at least 8 characters
      if len(password) < 8:
         raise ValidationError("Password must be at least 8 characters long.")
        
        # Set password securely using set_password method
      user.set_password(password)
      user.save()

      return user

  def update(self, user: User) -> User:
    try:
      existing_user = User.objects.get(id=user.id)
      existing_user.username = user.username
      existing_user.user_type = user.user_type
      existing_user.email = user.email
      if user.password:
        existing_user.set_password(user.password)
      existing_user.save()

      # Log the update process
      logging.info(f"User {existing_user.username} updated successfully.")
      return existing_user

    except User.DoesNotExist:
      logging.error(f"User with id {user.id} does not exist.")
      return None

  def delete(self, user_id: int) -> bool:
    try:
      user = User.objects.get(id=user_id)
      user.delete()

      # Log the deletion process
      logging.info(f"User with id {user_id} deleted successfully.")
      return True
    except User.DoesNotExist:
      logging.error(f"User with id {user_id} does not exist.")
      return False
  def update_user_role(self, user_id: int, new_role: str) -> User:
        # Validate that the new role is a valid choice
        # if new_role not in [User.UserRole.ADMIN, User.UserRole.CUSTOMER, User.UserRole.SUPPLIER]:
        #     raise ValidationError("Invalid role")

        try:
            # Retrieve the user by ID
            user = User.objects.get(id=user_id)
            
            # Update the user's role
            user.user_type = new_role
            user.save()  # Save the updated user
            
            return user  # Return the updated user
        except User.DoesNotExist:
            raise ValidationError(f"User with ID {user_id} does not exist.")