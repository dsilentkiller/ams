from django.db import models
from django.db.models import CASCADE
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, email, fullName, phoneNumber, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        # Use default password if not provided
        if not password:
            password = "password@123"

        # Hash the password
        hashed_password = make_password(password)

        user = self.model(email=email, fullName=fullName,
                          phoneNumber=phoneNumber, role=role, password=hashed_password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullName, phoneNumber, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, fullName, phoneNumber, password, **extra_fields)


class Users(AbstractBaseUser):
    ROLE_CHOICES = (
        ('teacher', 'teacher'),
        ('admin', 'admin'),

    )
    fullName = models.CharField(
        max_length=200, blank=False, null=False, default="Ram Khadka", help_text="Enter your full name")
    email = models.EmailField(
        verbose_name="Email",
        null=False,
        max_length=255,
        unique=True,
        help_text="Enter your Email"
    )
    password = models.CharField(
        max_length=14, blank=False, null=False, help_text="Enter your password")
    is_active = models.BooleanField(default=True, null=False)
    is_admin = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    phoneNumber = models.CharField(
        max_length=14,
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^(\+\d{1,2}\s?)?\d{7,10}$',
                message="Phone number must be entered in the format '+977 9823456789'. Up to 15 digits allowed."
            ),
        ],
        help_text="Phone number in the format '+977 9823456789'. Up to 15 digits allowed."
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullName", "phoneNumber"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
