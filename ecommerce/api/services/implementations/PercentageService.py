from api.Mapper.PercentageMapper import PercentageMapper
from api.repositories.interfaces.IpercentageRepository import IPercentageRepository
from api.services.interfaces.IPercentageService import IPercentageService
from api.dto.percentage_dto import PercentageDTO
from api.wrpper.result import ConcreteResultT, ResultT

class PercentageService(IPercentageService):
    def __init__(self, percentage_repository: IPercentageRepository):
        self.percentage_repository = percentage_repository

    def get_by_id(self, id: int) -> ResultT:
        try:
            percentage = self.percentage_repository.get_by_id(id)
            if percentage:
                dto = PercentageMapper.to_dto(percentage)
                return ConcreteResultT.success(dto)
            return ConcreteResultT.fail("Percentage not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving percentage: {str(e)}", 500)

    def all(self) -> ResultT:
        try:
            percentages = self.percentage_repository.all()
            if percentages:
                dto_list = PercentageMapper.to_dto_list(percentages)
                return ConcreteResultT.success(dto_list)
            return ConcreteResultT.fail("No percentages found", 200)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving percentages: {str(e)}", 500)

    def add(self, percentage_dto: PercentageDTO) -> ResultT:
        try:
            # Convert DTO to model
            model = PercentageMapper.to_model(percentage_dto)

            # Check if the supplier already has a percentage
            existing_percentage = self.percentage_repository.get_by_supplier(model.supplier_id)
            if existing_percentage:
                # Return failure if supplier already exists with a percentage
                return ConcreteResultT.fail("Supplier already exists with a percentage", 400)

            # Add the new percentage
            res = self.percentage_repository.add(model)
            if res:
                return ConcreteResultT.success("Percentage added successfully")
            return ConcreteResultT.fail("Failed to add percentage", 500)

        except Exception as e:
            return ConcreteResultT.fail(f"Failed to add percentage: {str(e)}", 500)

    def update(self, percentage_dto: PercentageDTO) -> ResultT:
        try:
            model = PercentageMapper.to_model(percentage_dto)
            res = self.percentage_repository.update(model)
            if res:
                return ConcreteResultT.success("Percentage updated successfully")
            return ConcreteResultT.fail("Failed to update percentage", 500)
        except Exception as e:
            return ConcreteResultT.fail(f"Failed to update percentage: {str(e)}", 500)

    def delete(self, percentage_dto: PercentageDTO) -> ResultT:
        try:
            model = self.percentage_repository.get_by_id(percentage_dto.id)
            if model:
                if self.percentage_repository.delete(model):
                    return ConcreteResultT.success("Percentage successfully deleted", 200)
                return ConcreteResultT.fail("Failed to delete percentage", 400)
            return ConcreteResultT.fail("Percentage not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)

    def assign_percentage_value_to_suppliers(self, market_id: int) -> ResultT:
        try:
            result = self.percentage_repository.assign_percentage_value_to_suppliers(market_id)
            if result == 1:
                return ConcreteResultT.fail("Percentage value already assigned", 200)
            elif result == 2:
                return ConcreteResultT.success("Percentage value assigned to suppliers successfully")
            else:
                return ConcreteResultT.fail("An error occurred while assigning percentage value", 500)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during percentage assignment: {str(e)}", 500)
