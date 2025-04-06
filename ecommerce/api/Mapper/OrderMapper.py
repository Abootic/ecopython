from django.apps import apps
from api.dto.order_dto import OrderDTO
from datetime import date, datetime

class OrderMapper:

    @staticmethod
    def convert_to_dto(order) -> OrderDTO:
        """
        Convert the Order model to OrderDTO.
        """
        return OrderDTO(
            id=order.id,
            customer_id=order.customer.id if order.customer else None,
            product_id=order.product.id if order.product else None,
            total_price=float(order.total_price) if order.total_price is not None else 0.0,  
            price=float(order.price) if order.price is not None else 0.0,  
            quantity=order.quantity,
            create_at=(
                order.create_at.isoformat()  
                if isinstance(order.create_at, (date, datetime)) 
                else datetime.now().isoformat()  
            )
        )

    @staticmethod
    def convert_to_model(order_dto: OrderDTO):
        """
        Convert the OrderDTO to an Order model.
        """
        Order = apps.get_model('api', 'Order')
        return Order(
            id=order_dto.id,
            customer_id=order_dto.customer_id,
            product_id=order_dto.product_id,
            total_price=order_dto.total_price,
            price=order_dto.price,
            quantity=order_dto.quantity,
            create_at=order_dto.create_at  # You may need to adjust the date format here
        )