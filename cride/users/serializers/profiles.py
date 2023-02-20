"""Profile serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = '__all__'

        read_only_fields = (
            'rides_taken',
            'rides_offered',
            'reputation',
        )