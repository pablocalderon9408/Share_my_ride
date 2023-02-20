"""Membership serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership

# Serializers
from cride.users.serializers import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    user = UserModelSerializer(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)
    invited_by = serializers.StringRelatedField()

    class Meta:
        """Meta class."""

        model = Membership
        fields = (
            'user',
            'is_admin',
            'is_active',
            'used_invitations',
            'remaining_invitations',
            'rides_taken',
            'rides_offered',
            'joined_at',
            'invited_by',
        )

        read_only_fields = (
            'user',
            'used_invitations',
            'remaining_invitations',
        )
