"""Users views."""

# Django REST Framework
from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

# Permissions
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from cride.users.permissions import IsAccountOwner

from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
    )

# Models
from cride.users.models import User
from cride.circles.models import Circle

# Serializers
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import ProfileModelSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """User view set
    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = []
        if self.action in ['signup', 'login', 'verify']:
            permissions.append(AllowAny)
        elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
            permissions.append(IsAuthenticated)
            permissions.append(IsAccountOwner)
        else:
            permissions.append(IsAuthenticated)
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'status': 'ok',
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'status': 'ok',
            'user': UserModelSerializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'message': 'Congratulations, now go share some rides!',
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response
    
    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)