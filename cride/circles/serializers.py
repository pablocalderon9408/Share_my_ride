"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from cride.circles.models import Circle

class CircleSerializer(serializers.Serializer):
    """Circle serializer."""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()

    def create(self, data):
        """Handle circle creation."""
        return Circle.objects.create(**data)

    def update(self, instance, data):
        """Handle circle update."""
        instance.name = data.get('name', instance.name)
        instance.slug_name = data.get('slug_name', instance.slug_name)
        instance.about = data.get('about', instance.about)
        instance.save()
        return instance
    

class CreateCircleSerializer(serializers.Serializer):
    """Create circle serializer."""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[UniqueValidator(queryset=Circle.objects.all())]
    )
    about = serializers.CharField(max_length=255, required=False)

    def validate_slug_name(self, data):
        """Verify slug name is unique."""
        circle = Circle.objects.filter(slug_name=data)
        if circle.exists():
            raise serializers.ValidationError('Circle slug name already in use.')
        return data

    def create(self, data):
        """Handle circle creation."""
        return Circle.objects.create(**data)