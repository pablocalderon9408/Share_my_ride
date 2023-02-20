"""Circle members views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

# models
from cride.circles.models import Membership, Circle

# Serializers
from cride.circles.serializers import MembershipModelSerializer


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Circle Membership view set."""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)
    
    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]

        return [p() for p in permissions]
    
    def get_queryset(self):
        """Return circle members."""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )
    
    def get_object(self):
        """Return the circle member by using the user's username."""
        return get_object_or_404(
            Membership,
            circle=self.circle,
            user__username=self.kwargs['pk'],
            is_active=True
        )
    
    def perform_destroy(self, instance):
        """Disable membership."""
        instance.is_active = False
        instance.save()
        data = MembershipModelSerializer(instance).data
        return Response(data, status=status.HTTP_204_NO_CONTENT)
