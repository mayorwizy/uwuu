from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, reg_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            reg_number=reg_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, reg_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            reg_number=reg_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Position(models.Model):
    position = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.position


class LGA(models.Model):
    lga = models.CharField(null=True, max_length=100)

    class Meta:
        verbose_name = 'Local Govt. Area'
        verbose_name_plural = 'Local Govt. Areas'

    def __str__(self):
        return self.lga


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    reg_number = models.IntegerField(null=True, blank=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'reg_number']

    objects = MyAccountManager()

    class Meta:
        verbose_name = 'Registered Member'
        verbose_name_plural = 'Registered Members'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Month(models.Model):
    month = models.CharField(max_length=20)

    def __str__(self):
        return self.month


class Year(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, null=True, blank=True)
    occupation = models.CharField(null=True, blank=True, max_length=100)
    gender_choice = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=50, null=True, choices=gender_choice)
    dob = models.DateField(null=True, blank=True)
    marital_status_choice = (
        ('Single(Never Married)', 'Single(Never Married)'),
        ('Engaged', 'Engaged'),
        ('Married', 'Married'),
        ('Seperated', 'Seperated'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),

    )
    marital_status = models.CharField(
        null=True, max_length=100, choices=marital_status_choice)
    position = models.ForeignKey(
        Position, default='Member', null=True, on_delete=models.CASCADE)
    lga = models.ForeignKey(
        LGA, null=True, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True, max_length=200)
    profile_pic = models.ImageField(
        null=True, blank=True, default='default.png', upload_to='profile_photos')

    def __str__(self):
        return str(self.user)


class Dues(models.Model):
    account_holder = models.ForeignKey(Account, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.DO_NOTHING)
    year = models.ForeignKey(Year, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Due'
        verbose_name_plural = 'Dues'

    def __str__(self):
        return str(self.account_holder)
