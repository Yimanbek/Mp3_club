from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Email should be provided')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('A staff user must have is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('A superuser must have is_superuser=True')
        return self._create_user(email, password, **kwargs)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False, help_text='This field is to activate the user')
    activation_code = models.CharField(max_length=255, blank=True)
    password_change_code = models.CharField(max_length=255, blank=True)
    is_author = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

    def create_number_code(self):
        code = get_random_string(6, allowed_chars='1234567890')
        self.password_change_code = code
        return code