class ProductDTO:
    def __init__(self, id=None, name=None, price=None, supplier_id=None, image=None, user_id=None):
        self.id = id
        self.name = name
        self.price = price
        self.supplier_id = supplier_id
        self.image = image
        self.user_id = user_id  # Added user_id attribute

    @classmethod
    def from_model(cls, product):
        # Map fields from the product model to the ProductDTO
        return cls(
            id=product.id,
            name=product.name,
            price=product.price,
            supplier_id=product.supplier_id,
            image=product.image,
            user_id=product.user_id  # Map user_id
        )

    def to_dict(self):
        # Ensure that the returned dictionary is serializable
        return {
            'id': self.id,
            'name': self.name,
            'price': str(self.price),  # Ensure that price is serializable
            'supplier_id': self.supplier_id,
            "image": self.image,
            "user_id": self.user_id  # Include user_id in the dictionary
        }