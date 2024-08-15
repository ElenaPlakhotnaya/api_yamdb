from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from .constants import MAX_LENGTH_NAME, SLICE_NAME
from .validators import validate_username, username_is_not_forbidden

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        validators=[validate_username, username_is_not_forbidden],
        verbose_name='Имя пользователя',
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    role = models.CharField(
        default=USER,
        choices=ROLES,
        max_length=max(len(role) for role, _ in ROLES),
        verbose_name='Роль'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        verbose_name='Фамилия'
    )
    confirmation_code = models.CharField(
        max_length=settings.CONF_CODE_MAX_LEN,
        default=settings.DEFAULT_CONF_CODE,
        verbose_name='Код подтверждения'
    )

    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_email_username'
            )
        ]

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff

    def __str__(self):
        return self.username[:SLICE_NAME]
