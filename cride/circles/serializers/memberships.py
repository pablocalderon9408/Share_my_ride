"""Membership serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership, Invitation

# Serializers
from cride.users.serializers import UserModelSerializer

# Utilities
from django.utils import timezone


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


class AddMemberSerializer(serializers.Serializer):
    """Add member serializer.

    Handle the addition of a new member to a circle.
    Circle object must be provided in the context.

    The serializer is able to identify the user because
    in the context there is a request object.
    """

    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        """Verify user isn't already a member."""
        circle = self.context['circle']
        member = Membership.objects.filter(circle=circle, user=data)
        if member.exists():
            raise serializers.ValidationError('User is already member of the circle.')
        return data

    def validate_invitation_code(self, data):
        """Verify code exists and it is related to the circle."""
        circle = self.context['circle']
        try:
            invitation = Invitation.objects.get(
                code=data,
                circle=self.context['circle'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context["invitation"] = invitation
        return data
    
    def validate(self, data):
        """Verify circle allows new members."""
        circle = self.context['circle']
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('Circle has reached its member limit.')
        return data

    def create(self, data):
        """Handle member creation."""
        circle = self.context['circle']
        invitation = self.context['invitation']
        user = data['user']
        now = timezone.now()
        import ipdb; ipdb.set_trace()
        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by
        )

        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        # Update issuer data
        issuer = Membership.objects.get(user=invitation.issued_by, circle=circle)
        issuer.used_invitations += 1
        issuer.remaining_invitations -= 1
        issuer.save()

        return member

        return member