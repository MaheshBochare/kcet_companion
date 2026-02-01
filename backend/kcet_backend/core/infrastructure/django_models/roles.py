from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="USER"):
        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=self.normalize_email(email),
            role=role,
        )
        user.set_password(password or "")
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
            role="OWNER",
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_approved = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_OWNER = "OWNER"
    ROLE_ADMIN = "ADMIN"
    ROLE_USER = "USER"

    ROLE_CHOICES = [
        (ROLE_OWNER, "Owner"),
        (ROLE_ADMIN, "Admin"),
        (ROLE_USER, "User"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    # 🔐 AUTH FLAGS
    is_active = models.BooleanField(default=True)   # Django internal
    is_staff = models.BooleanField(default=False)

    # ✅ APPROVAL FLAG (NEW)
    is_approved = models.BooleanField(default=False)

    # 🔢 OTP
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)

    # 🔑 SINGLE SESSION
    current_session_id = models.UUIDField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"
