"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from cride.circles.models import Circle
    

class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer."""

    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000
    )

    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta class."""
        model = Circle
        fields = (
            'name',
            'slug_name',
            'about',
            'rides_taken',
            'rides_offered',
            'verified',
            'is_public',
            'members_limit',
            'is_limited'
        )
        read_only_fields = (
            'is_public',
            'verified',
            'rides_taken',
            'rides_offered'
        )

    def validate(self, data):
        """Ensure both members_limit and is_limited are present."""
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limited, a member limit must be provided.')
        return data
