from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You need to provide an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_tutor", True)
        extra_fields.setdefault("is_manager", True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, unique=True)
    username = models.CharField(max_length=100, blank=True, default="")
    organisation = models.CharField(max_length=100, blank=True, default="")

    is_active = models.BooleanField(blank=True, default=True)
    is_superuser = models.BooleanField(blank=True, default=False)
    is_staff = models.BooleanField(blank=True, default=False)

    date_joined = models.DateField(blank=True, default=timezone.now)

    is_tutor = models.BooleanField(blank=True, default=False)
    is_student = models.BooleanField(blank=True, default=True)
    is_manager = models.BooleanField(blank=True, default=False)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def clean(self):
        """
        A CustomUser can be either
            1. a superuser
            2. a manager/admin (managers can be tutors and/or students)
            3. EITHER a tutor OR a student
        """
        if self.is_superuser or self.is_manager:
            return
        if self.is_tutor ^ self.is_student:
            return

        raise ValidationError(
            "A user must be one of the following: "
            "superuser, "
            "manager, "
            "or either a tutor or a student"
        )

    def __str__(self):
        if self.is_superuser:
            return f"Superuser: {self.email}"
        if self.is_tutor:
            return f"Tutor: {self.email}"
        if self.is_student:
            return f"Student: {self.email}"
        if self.is_manager:
            return f"Manager: {self.email}"
        return f"User: {self.email}"


class TeachesManager(models.Manager):
    """
    Adds (tutor_id, student_id) pair to Teaches table
    Returns whether operation was a success or not along with the error message
            if operation failed
    """

    def add_teaching_relationship(self, tutor_id, student_id):
        # Retrieve users from CustomUser relation
        try:
            tutor = CustomUser.objects.get(pk=tutor_id)
            student = CustomUser.objects.get(pk=student_id)
        except ObjectDoesNotExist as e:
            return False, str(e)

        # Perform check
        if not tutor.is_tutor:
            return False, "Tutor is not a tutor"
        if not student.is_student:
            return False, "Student is not a student"

        try:
            self.create(tutor_id=tutor_id, student_id=student_id)
            return True, None
        except IntegrityError as e:
            return False, str(e)

    """
    Removes (tutor_id, student_id) pair from Teaches table
    Returns whether operation was a success or not along with the error message
            if operation failed
    """

    def remove_teaching_relationship(self, tutor_id, student_id):
        try:
            relationship: Teaches = self.get(tutor_id=tutor_id, student_id=student_id)
            relationship.delete()
            return True, None
        except Teaches.DoesNotExist:
            return False, "The teaching relationship does not exist"

    def get_students_by_tutor_id(self, tutor_id):
        return self.filter(tutor_id=tutor_id).values_list("student_id", flat=True)

    def get_tutors_by_student_id(self, student_id):
        return self.filter(student_id=student_id).values_list("tutor_id", flat=True)


class Teaches(models.Model):
    tutor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tutor_relationships"
    )
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_relationships"
    )

    objects = TeachesManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tutor", "student"], name="unique_tutor_student_constraint"
            )
        ]

    def __str__(self):
        return (
            f"Tutor {str(self.tutor.email)} teaches Student {str(self.student.email)}"
        )
