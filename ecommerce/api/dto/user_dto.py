class UserDTO:
    def __init__(self, id=None, username=None, email=None, user_type=None, password=None):
        self.id = id
        self.username = username
        self.user_type = user_type
        self.email = email
        self.password = password  # password is for internal use, not included in serialized output
    
    @staticmethod
    def from_model(user):
        """Convert a User model instance to a UserDTO."""
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            user_type=user.user_type  # Assuming 'user_type' is a field in your custom User model
        )
    
    def to_dict(self):
        """Convert the UserDTO to a dictionary to make it JSON serializable."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type
        }
