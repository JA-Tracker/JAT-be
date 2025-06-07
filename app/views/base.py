from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet that provides default CRUD operations.
    """
    pass