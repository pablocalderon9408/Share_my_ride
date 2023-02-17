"""Circles views."""

# Django
from django.http import HttpResponse, JsonResponse

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

# Serializers
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer

# Models
from cride.circles.models import Circle

@api_view(['GET'])
def list_circles(request):
    """List circles."""
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(data=serializer.data, status=200)


@api_view(['POST'])
def create_circle(request):
    """Create circle."""
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    data = CircleSerializer(circle).data
    return Response(data, status=201)
