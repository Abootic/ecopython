from abc import ABC, abstractmethod

class loginResultT(ABC):
    def __init__(self, status, data):
        self.status = status
        self.data = data

    @abstractmethod
    def success(cls, data):
        pass

    @abstractmethod
    def fail(cls, message, code):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class loginResult:
    def __init__(self, message, code, succeeded):
        self.message = message
        self.code = code
        self.succeeded = succeeded


class LoginesultT(loginResultT):
    def __init__(self, status: loginResult, data):
        super().__init__(status, data)

    @classmethod
    def success(cls, data, message="success"):
        # Create a success status with a custom message and code 200
        status = loginResult(message, 200, True)
        return cls(status, data)

    @classmethod
    def fail(cls, message, code):
        # Ensure you pass both the message and the code
        status = loginResult(message, code, False)
        return cls(status, None)
    @classmethod
    def loginfail(cls, message: str, code: int):
        """A separate method specifically for login failures."""
        status = loginResult(message=message, code=code, succeeded=False)
        return cls(status, None)

    def to_dict(self):
        # Convert the status and data into a dictionary format
        return {
            "success": self.status.succeeded,
            "message": self.status.message,
            "data": self.data,
            "status_code": self.status.code
        }
    
