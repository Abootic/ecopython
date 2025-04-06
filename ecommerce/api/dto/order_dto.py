from datetime import datetime

class OrderDTO:
    def __init__(self, id=None, customer_id=None, product_id=None, total_price=None, price=None, quantity=None, create_at=None):
        self.id = id if id is not None else None
        self.customer_id = customer_id
        self.product_id = product_id
        self.total_price = total_price
        self.price = price
        self.quantity = quantity

        # Ensure create_at is a datetime object
        if isinstance(create_at, str):
            try:
                self.create_at = datetime.fromisoformat(create_at)  # Convert from string to datetime
            except ValueError:
                self.create_at = datetime.now()  # Fallback to current time if parsing fails
        elif isinstance(create_at, datetime):
            self.create_at = create_at
        else:
            self.create_at = datetime.now()  # Default to current time

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "total_price": str(self.total_price),
            "price": str(self.price),
            "quantity": self.quantity,
            "create_at": self.create_at.isoformat()  # Now it will always be a datetime object
        }
