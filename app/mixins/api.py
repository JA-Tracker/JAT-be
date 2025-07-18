from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        """
        Create a standardized success response
        """
        response_data = {}
        if data is not None:
            response_data['data'] = data
        if message is not None:
            response_data['message'] = message
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST, errors=None):
        """
        Create a standardized error response
        """
        response_data = {'error': message}
        if errors is not None:
            response_data['details'] = errors
        return Response(response_data, status=status_code)