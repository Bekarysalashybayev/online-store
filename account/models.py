import datetime
import hashlib
import os

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.db import models

from OnlineStore import settings


class Role(models.Model):
    name = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     **extra_fields):
        """
        Create and save a User with given phone_number, email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None,
                    **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True, )
    name = models.CharField(_('first name'), max_length=150, blank=True)
    surname = models.CharField(_('last name'), max_length=150, blank=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE, default=2, null=True, blank=True)
    icon = models.ImageField(upload_to='images/', blank=True, null=True)
    phone = models.CharField(max_length=255, unique=True, blank= True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin'
                    ' site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return " ".join([self.name, self.surname])


class EmailToken(models.Model):
    email = models.CharField(max_length=10)
    otp = models.CharField(max_length=40, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "OTP Token"
        verbose_name_plural = "OTP Tokens"

    @classmethod
    def create_otp_for_number(cls, email):
        # The max otps generated for a number in a day are only 10.
        # Any more than 10 attempts returns False for the day.
        today_min = datetime.datetime.combine(datetime.date.today(),
                                              datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(),
                                              datetime.time.max)
        otps = cls.objects.filter(email=email,
                                  timestamp__range=(today_min, today_max))
        if otps.count() <= 10:
            otp = cls.generate_otp(length=4)
            email_otp = EmailToken(email=email, otp=otp)
            email_otp.save()
            text = "Online-store платформасына кіру: " + str(otp) + "\n" + "Жіберілген СМС 1 минут ішінде жарамды."
            send_mail(
                'Online-store',
                text,
                settings.EMAIL_HOST_USER,
                [email],
            )
            return email_otp
        else:
            return False

    @classmethod
    def generate_otp(cls, length=4):
        hash_algorithm = 'sha256'
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp

    def __str__(self):
        return "{} - {}".format(self.email, self.otp)
