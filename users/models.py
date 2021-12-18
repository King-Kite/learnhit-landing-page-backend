from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now
from django_countries.fields import CountryField
from .managers import UserManager

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name='first name', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150, blank=True)
    middle_name = models.CharField(verbose_name='middle name', max_length=150, blank=True)
    premium = models.BooleanField(default=False)
    premium_expiration_date = models.DateTimeField(verbose_name='premium expiration date', 
        help_text="Specifies the expiration date of access to premium content", blank=True, null=True)
    premium_life = models.BooleanField(verbose_name='premium for life', default=False, help_text='Specifies whether a user has access to premium content for life')
    is_active = models.BooleanField(default=True, help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
            ))
    is_course_creator = models.BooleanField(default=False, help_text=(
            'Designates whether this user should be treated as a course creator. '
            ))
    is_publisher = models.BooleanField(default=False, help_text=(
            'Designates whether this user should be treated as a publisher. '
            ))
    is_admin = models.BooleanField(default=False, help_text=(
            'Designates whether this user is a staff and can log into the admin site. '
            ))
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_premium_user(self):
        "Is the user premium user?"
        return self.premium

    @property
    def has_premium_expired(self):
        if self.premium is True:
            if self.premium_life is True or self.premium_expiration_date > now():
                return False
        self.premium = False
        self.save()
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to="images/users/profile", default="images/users/profile/default.png")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = CountryField(blank_label='(select country)', default='NG')
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} profile"
