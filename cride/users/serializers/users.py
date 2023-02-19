"""User serializers."""
# JWT
import jwt

# Utils
from datetime import timedelta

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

# Models
from cride.users.models import User, Profile


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User signup serializer."""
    
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        min_length=4,
        max_length=50,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be enered in the format: +999999999999. Up to 15 digits allowed"
    )

    phone_number = serializers.CharField(min_length=7, max_length=20, validators=[phone_regex])

    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=50)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user creation."""
        data.pop('password_confirmation')
        # Create user is an special method.
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user
    
    def send_confirmation_email(self, user):
        """Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        # Done based on Django documentation:
        # https://docs.djangoproject.com/en/4.1/topics/email/#sending-alternative-content-types
        subject= f'Welcome @{user.username}'
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            template_name="emails/users/account_verification.html", 
            context={
                'user': user,
                'token': verification_token
            }
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()
        return print("Send confirmation email to: {}".format(user.email))

    def gen_verification_token(slef, user):
        """Create JWT token that the user can use to verify its account."""
        expiration_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(expiration_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(.')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

    def update(self, instance, data):
        """Assign new token to user."""
        pass


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token.')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token.')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()