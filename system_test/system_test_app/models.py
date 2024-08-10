import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser):
    name = models.CharField(max_length=20)
    phone_number = models.IntegerField(unique=True)
    is_teacher = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Subjects(models.Model):
    name = models.CharField(max_length=25)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Theme(models.Model):
    name = models.CharField(max_length=70)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Tests(models.Model):
    theme_id = models.ForeignKey(Theme, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Answers(models.Model):
    tests_id = models.ForeignKey(Tests, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_true = models.BooleanField(default=False)

class Activate(models.Model):
    id_test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(auto_now_add=True)

class Action(models.Model):
    id_student = models.ForeignKey(User, on_delete=models.CASCADE)
    id_activated = models.ForeignKey(Activate, on_delete=models.CASCADE)