from api.services.interfaces.ISupplierProfitService import ISupplierProfitService
from api.repositories.interfaces.ISupplierProfitRepository import ISupplierProfitRepository
from api.wrpper.result import ConcreteResultT, ResultT
from api.dto.supplierProfit_dto import SupplierProfitDTO

class SupplierProfitService(ISupplierProfitService):
    def __init__(self, repository:ISupplierProfitRepository):
        self._repository = repository

    def all(self) -> ResultT:
        try:
            res = self._repository.all()
            if res:
                obj = [SupplierProfitDTO.from_model(r) for r in res]
                return ConcreteResultT.success(obj)
            return ConcreteResultT.fail("No profit found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving profit: {str(e)}", 500)
    def update_or_create_profit(self, market_id, month):
        """
        Calculate and save the profit for each supplier in a market for a given month.
        """
        try:
            # Step 1: Calculate total profit for the market (sum of all order prices for the month)
            total_profit = self._repository.get_total_profit_for_market(market_id, month)

            if total_profit is None:
                return ConcreteResultT.fail(f"No profit data found for market {market_id} in {month}.", 404)

            print(f"Total Profit for Market {market_id} in {month}: {total_profit}")

            # Step 2: Get the supplier percentages for the market
            supplier_percentages = self._repository.get_supplier_percentages(market_id)

            if supplier_percentages.count() == 0:
                return ConcreteResultT.fail(f"No supplier data found for market {market_id}.", 404)

            print(f"Supplier Percentages: {supplier_percentages.count()} suppliers found.")

            # Step 3: Calculate and update/create profit for each supplier
            for sp in supplier_percentages:
                supplier_profit = (total_profit * sp.percentage_value) / 100  # Calculate profit based on percentage

                print(f"Supplier {sp.supplier.id} Profit: {supplier_profit}")

                # Update or create the profit entry for the supplier
                self._repository.update_or_create_supplier_profit(
                    supplier=sp.supplier,  # Pass the supplier object
                    month=month,           # Pass the month
                    profit=supplier_profit # Pass the calculated profit
                )

            return ConcreteResultT.success(f"Profit calculation completed for market {market_id} for {month}.")
        
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during profit calculation: {str(e)}", 500)

    