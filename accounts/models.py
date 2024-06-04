from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
# Create your models here.


class UserManager(BaseUserManager):
    # user create function
    def create_user(self, email, fullName, phoneNumber, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        # use default password if not provided
        if not password:
            password = "password@123"
        # hash password
        hashed_password = make_password(password)
        user = self.model(email=email, fullName=fullName,
                          phoneNumber=phoneNumber, password=hashed_password, **extra_fields)
        user.save(using=self._db)
        return user
    # superuser create function

    def create_superuser(self, email, fullName, phoneNumber, password=None, **extra_fields):
        
        
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, fullName, phoneNumber, password, **extra_fields)


class Users(AbstractBaseUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),

    )

    fullName = models.CharField(
        max_length=255, help_text="fullName is required", null=False, blank=False)
    email = models.EmailField(
        unique=True, null="False", blank="False", help_text="email field required")
    password = models.CharField(max_length=50,
        null="False", blank="False", help_text="enter your password")
    course = models.CharField(
        max_length=255, blank=False, null=False, help_text="course is required")
    phoneNumber = models.CharField(
        max_length=14, blank=False, null=False, help_text="phone number is required")
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName', 'phoneNumber']
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    objects = UserManager()

    # def __str__(self):
    #     return self.fullName
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):  # admin
        return self.is_admin

    def has_module_perms(Self, app_label):
        return True
    def has_perm(self,perm,obj=None):
        return self.is_superuser
    
    def has_module_perms(self,app_label):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_admin
