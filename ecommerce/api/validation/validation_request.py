from rest_framework.response import Response

class ValidationRequest:
    @staticmethod
    def validate_request_data(request_data, required_fields):
        """Validates required fields in request data."""
        missing_fields = [field for field in required_fields if field not in request_data]
        if missing_fields:
            print(f"Error: Missing fields: {missing_fields}")
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400)
        return None
