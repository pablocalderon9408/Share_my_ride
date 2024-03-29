"""Circle invitation manager."""

# Django
from django.db import models

# Utilities
import random
from string import ascii_uppercase, digits


class InvitationManager(models.Manager):
    """Invitation manager.
    
    Use to handle code creation."""

    CODE_LENGTH = 10

    def create(self, **kwargs):
        """Create invitation."""
        pool = ascii_uppercase + digits + '-.'
        code = kwargs.get("code", ''.join(random.choices(pool, k=self.CODE_LENGTH)))
        while self.filter(code=code).exists():
            code = ''.join(random.choices(pool, k=self.CODE_LENGTH))
        kwargs["code"] = code
        print(code)
        return super(InvitationManager, self).create(**kwargs)
