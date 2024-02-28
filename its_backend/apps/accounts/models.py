from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You need to provide an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email: str | None, password: str | None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_tutor', True)
        extra_fields.setdefault('is_manager', True)
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(max_length=100, blank=True, default='')
    organisation = models.CharField(max_length=100, blank=True, default='')
    
    is_active = models.BooleanField(blank=True, default=True)
    is_superuser = models.BooleanField(blank=True, default=False)
    is_staff = models.BooleanField(blank=True, default=False)

    date_joined = models.DateField(blank=True, default=timezone.now)

    is_tutor = models.BooleanField(blank=True, default=False)
    is_student = models.BooleanField(blank=True, default=True)
    is_manager = models.BooleanField(blank=True, default=False)

    class Meta:
        '''
        A CustomUser can be either
            1. a superuser
            2. a manager/admin (managers can be tutors and/or students)
            3. EITHER a tutor OR a student
        '''
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(is_superuser=True) |
                    models.Q(is_manager=True) |
                    (models.Q(is_tutor=True) ^ models.Q(is_student=True))
                ),
                name='user_role_constraint'
            )
        ]

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        if self.is_superuser:
            return f"Superuser: {self.email}"
        elif self.is_tutor:
            return f"Tutor: {self.email}"
        elif self.is_student:
            return f"Student: {self.email}"
        elif self.is_manager:
            return f"Manager: {self.email}"
        else: 
            return f"User: {self.email}"