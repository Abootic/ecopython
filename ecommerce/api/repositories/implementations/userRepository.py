import logging
from django.core.exceptions import ValidationError
from api.models.user import User
from api.repositories.interfaces.IUserRepository import IUserRepository
from api.repositories.implementations.GenericRepository import GenericRepository

class UserRepository(GenericRepository[User], IUserRepository):

    def add(self, user: User, password: str) -> User:
        """Add a new user with password validation"""
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        user.set_password(password.strip())
        user.save()
        return user

    def update_user_role(self, user_id: int, new_role: str) -> User:
        """Update user role with validation"""
        try:
            user = self._model.objects.get(id=user_id)
            user.user_type = new_role
            user.save()
            logging.info(f"Updated role for user {user_id} to {new_role}")
            return user
        except self._model.DoesNotExist:
            logging.error(f"User with id {user_id} does not exist")
            raise ValidationError(f"User with ID {user_id} does not exist.")

    def update(self, user: User) -> User:
        """Custom update to handle password changes"""
        try:
            existing_user = self._model.objects.get(id=user.id)
            existing_user.username = user.username
            existing_user.user_type = user.user_type
            existing_user.email = user.email
            
            if user.password:
                existing_user.set_password(user.password)
                
            existing_user.save()
            logging.info(f"User {existing_user.username} updated")
            return existing_user
            
        except self._model.DoesNotExist:
            logging.error(f"User with id {user.id} does not exist")
            return None