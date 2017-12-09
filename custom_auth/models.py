from __future__ import unicode_literals

import random
import string
from datetime import timedelta
from django.utils import timezone

from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from panorbit import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    FEMALE = "Female"
    MALE = "Male"
    OTHERS = "Others"

    GENDER = (
        (FEMALE, "Female"),
        (MALE, "Male"),
        (OTHERS, "Others"),
    )
    email = models.EmailField(_('email address'), primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.CharField(_('gender'), max_length=6, choices=GENDER, default=FEMALE)
    phone_number = models.CharField(_('phone number'), blank=True, null=True, max_length=10)
    is_active = models.BooleanField(_('active'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def make_user_active(self):
        self.is_active = True
        self.save()

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


def generate_otp(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Otp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otp")
    code = models.CharField(max_length=6,null=True,blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def send_otp_as_mail(self):
        Otp.objects.filter(user=self.user).delete()
        self.code = generate_otp()
        subject = "OTP"
        to_email = [self.user.email]
        from_email = settings.EMAIL_HOST_USER
        context = {'code': self.code}
        html_content = render_to_string('custom_auth/login_email.html', context)
        msg = EmailMultiAlternatives(subject,"OTP", from_email, to_email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        self.save()
        return True

    def send_otp_as_sms(self):
        pass

    def is_active(self):
        timestamp = timezone.now() - timedelta(seconds=900)
        return self.time_stamp > timestamp



