from abc import ABC, abstractmethod

class ResultT(ABC):
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


class MessageResult:
    def __init__(self, message, code, succeeded):
        self.message = message
        self.code = code
        self.succeeded = succeeded


class ConcreteResultT(ResultT):
    def __init__(self, status: MessageResult, data):
        super().__init__(status, data)

    @classmethod
    def success(cls, data, message="success"):
        status = MessageResult(message, 200, True)
        return cls(status, data)

    @classmethod
    def fail(cls, message, code):
        status = MessageResult(message, code, False)
        return cls(status, None)

    @classmethod
    def loginfail(cls, message: str, code: int):
        status = MessageResult(message=message, code=code, succeeded=False)
        return cls(status, None)

    def to_dict(self):
        return {
            "success": self.status.succeeded,
            "message": self.status.message,
            "data": self.data,
            "status_code": self.status.code
        }
