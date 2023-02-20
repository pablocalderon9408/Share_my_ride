"""Circle views."""

# Django REST Framework
from rest_framework import mixins, viewsets, status

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsCircleAdmin

# Models
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers import CircleModelSerializer


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'
    paginate_by = 5

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [p() for p in permissions]

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
    
    # Important to know that this method was overriden because 
    # during the circle creation, a user must be assigned as the admin.
    # When you look the documentation of the ModelViewSet, you will see
    # that the perform_create method is called after the serializer is validated.
    # https://www.cdrf.co/3.13/rest_framework.mixins/CreateModelMixin.html
    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save(admin=self.request.user)
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )
