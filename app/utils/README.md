# API Utilities

This directory contains utility classes for standardizing API responses and error handling across the application.

## BaseAPIView

`BaseAPIView` is a base class that extends Django REST Framework's `APIView` and provides common functionality:

- Standardized error handling through the `handle_exception` method
- Serializer validation through the `validate_serializer` method
- Default authentication requirement with `IsAuthenticated` permission class

### Usage

```python
from ..utils.api import BaseAPIView, APIResponse

class MyAPIView(BaseAPIView):
    def get(self, request):
        # Your view logic here
        return APIResponse.success(data={'key': 'value'})
```

## APIResponse

`APIResponse` provides static methods for creating standardized API responses:

### Success Response

```python
APIResponse.success(
    data=your_data,  # Optional
    message="Operation successful",  # Optional
    status_code=status.HTTP_200_OK  # Optional, defaults to 200
)
```

Example success response:

```json
{
  "data": {
    "key": "value"
  },
  "message": "Operation successful"
}
```

### Error Response

```python
APIResponse.error(
    message="An error occurred",
    status_code=status.HTTP_400_BAD_REQUEST,  # Optional, defaults to 400
    errors=serializer.errors  # Optional, for validation errors
)
```

Example error response:

```json
{
  "error": "An error occurred",
  "details": {
    "field": ["This field is required."]
  }
}
```

## Serializer Validation

The `validate_serializer` method simplifies serializer validation:

```python
serializer_result = self.validate_serializer(
    serializer_class=MySerializer,
    data=request.data,
    instance=existing_instance,  # Optional, for updates
    partial=True  # Optional, for partial updates
)

if isinstance(serializer_result, MySerializer):
    # Validation passed, save the serializer
    instance = serializer_result.save()
    return APIResponse.success(data=MySerializer(instance).data)
else:
    # Validation failed, serializer_result is already an error response
    return serializer_result
```
