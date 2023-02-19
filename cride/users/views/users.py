"""Users views."""

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
    )

class UserLoginAPIView(APIView):
    """User login API view."""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'status': 'ok',
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserSignUpView(APIView):
    """User sign up API view."""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'status': 'ok',
            'user': UserModelSerializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerificationAPIView(APIView):
    """Account verification API view."""

    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congtulations, now go share some rides!',
        }
        return Response(data, status=status.HTTP_200_OK)