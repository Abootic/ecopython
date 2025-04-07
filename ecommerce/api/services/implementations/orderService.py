from api.Mapper.OrderMapper import OrderMapper
from api.dto.order_dto import OrderDTO
from api.repositories.interfaces.IOrderRepository import IOrderRepository
from api.services.interfaces.IorderService import IOrderService
from api.wrpper.result import ConcreteResultT, ResultT

from datetime import  datetime

class OrderService(IOrderService):

    def __init__(self, order_repository: IOrderRepository):
        self.order_repository = order_repository

    def get_by_id(self, order_id: int) -> ResultT:
        try:
            order = self.order_repository.get_by_id(order_id)
            if order:
                order_dto = OrderMapper.convert_to_dto(order)
                return ConcreteResultT.success(order_dto)
            else:
                return ConcreteResultT.fail("Order not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving order: {str(e)}", 500)

    def all(self) -> ResultT:
        try:
            orders = self.order_repository.all()
            if orders:
                order_dtos = [OrderMapper.convert_to_dto(order) for order in orders]
                return ConcreteResultT.success(order_dtos)
            else:
                return ConcreteResultT.fail("No orders found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving orders: {str(e)}", 500)

    def add(self, order: OrderDTO) -> ResultT:
        try:
            order_model = OrderMapper.convert_to_model(order)
            added_order = self.order_repository.add(order_model)
            if added_order:
                order_dto = OrderMapper.convert_to_dto(added_order)
                return ConcreteResultT.success(order_dto)
            else:
                return ConcreteResultT.fail("Failed to add order", 400)
        except Exception as e:
            return ConcreteResultT.fail(f"Error adding order: {str(e)}", 500)

    def update(self, order: OrderDTO) -> ResultT:
        try:
            order_model = OrderMapper.convert_to_model(order)
            updated_order = self.order_repository.update(order_model)
            if updated_order:
                order_dto = OrderMapper.convert_to_dto(updated_order)
                return ConcreteResultT.success(order_dto)
            else:
                return ConcreteResultT.fail("Failed to update order", 400)
        except Exception as e:
            return ConcreteResultT.fail(f"Error updating order: {str(e)}", 500)

    def delete(self, order: OrderDTO) -> ResultT:
        try:
            order_model = OrderMapper.convert_to_model(order)
            self.order_repository.delete(order_model)
            return ConcreteResultT.success("Order deleted successfully")
        except Exception as e:
            return ConcreteResultT.fail(f"Error deleting order: {str(e)}", 500)
    
    def get_orders_by_customer(self, customer_id: int) -> ResultT:
        print(" get_orders_by_customer service ")
        try:
            orders = self.order_repository.get_orders_by_customer(customer_id)
            for v in orders:
                print(f" in get_orders_by_customer in order service  ID: {v.id}, Product ID: {v.product_id}, Quantity: {v.quantity}, Price: {v.price}")
            if orders:
                order_dtos = [OrderMapper.convert_to_dto(order) for order in orders]
                return ConcreteResultT.success(order_dtos)
            else:
                return ConcreteResultT.fail("No orders found for this customer", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving orders for customer: {str(e)}", 500)

    def update_order_and_profit(self, order_id: int, new_price: float, new_quantity: int) -> ResultT:
        try:
            order = self.order_repository.get_by_id(order_id)
            if not order:
                return ConcreteResultT.fail("Order not found", 404)

            order.price = new_price
            order.quantity = new_quantity
            order.save()

            order_profit = new_price * new_quantity

            supplier = self.order_repository.get_supplier_by_product(order.product)
            if not supplier:
                return ConcreteResultT.fail("Supplier not found", 404)

            self.order_repository.update_or_create_supplier_profit(supplier, order_profit)
            return ConcreteResultT.success("Order and profit updated successfully")
        except Exception as e:
            return ConcreteResultT.fail(f"Error updating order and profit: {str(e)}", 500)

    def process_order(self, order_id: int) -> ResultT:
        try:
            self.calculate_supplier_profit(order_id)
            return ConcreteResultT.success("Order processed successfully")
        except Exception as e:
            return ConcreteResultT.fail(f"Error processing order: {str(e)}", 500)

    def get_supplier_profit_for_month(self, supplier_id: int) -> ResultT:
        try:
            profit = self.order_repository.get_supplier_profit_for_month(supplier_id)
            if profit is not None:
                return ConcreteResultT.success({
                    "month": datetime.now().date(),  # Assuming the current month
                    "profit": profit
                })
            else:
                return ConcreteResultT.fail("No profit found for this supplier in the given month", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving supplier profit: {str(e)}", 500)
   
    def calculate_supplier_profit(self, order_id: int) -> ResultT:
        try:
            # Implement your logic for calculating supplier profit based on the order
            return ConcreteResultT.success("Supplier profit calculated successfully")
        except Exception as e:
            return ConcreteResultT.fail(f"Error calculating supplier profit: {str(e)}", 500)
