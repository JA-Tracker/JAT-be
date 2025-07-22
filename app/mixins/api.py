from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK, cookies=None):
        """
        Create a standardized success response
        """
        response_data = {}
        if data is not None:
            response_data['data'] = data
        if message is not None:
            response_data['message'] = message
        response = Response(response_data, status=status_code)
        if cookies:
            for cookie in cookies:
                response.set_cookie(
                    key=cookie.get('key'),
                    value=cookie.get('value'),
                    httponly=cookie.get('httponly', True),
                    secure=cookie.get('secure', True),
                    samesite=cookie.get('samesite', 'Lax'),
                    max_age=cookie.get('max_age'),
                    expires=cookie.get('expires'),
                    path=cookie.get('path', '/'),
                    domain=cookie.get('domain'),
                )
        return response

    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST, errors=None, cookies=None):
        """
        Create a standardized error response
        """
        response_data = {'error': message}
        if errors is not None:
            response_data['details'] = errors
        response = Response(response_data, status=status_code)
        if cookies:
            for cookie in cookies:
                response.set_cookie(
                    key=cookie.get('key'),
                    value=cookie.get('value'),
                    httponly=cookie.get('httponly', True),
                    secure=cookie.get('secure', True),
                    samesite=cookie.get('samesite', 'Lax'),
                    max_age=cookie.get('max_age'),
                    expires=cookie.get('expires'),
                    path=cookie.get('path', '/'),
                    domain=cookie.get('domain'),
                )
        return response