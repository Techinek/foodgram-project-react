from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = {
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    }
    email = models.EmailField(
            max_length=254,
            unique=True,
            blank=False,
            error_messages={
                'unique':'Пользователь с таким email уже существует!',
            },
    )
    username = models.CharField(
            max_length=150,
            unique=True,
            error_messages={
                'unique':'Пользователь с таким никнеймом уже существует!',
            },
    )
    first_name = models.CharField(
            max_length=150,
            blank=True,
    )
    last_name = models.CharField(
            max_length=150,
            blank=True,
    )
    role = models.CharField(
            max_length=20,
            choices=ROLES,
            default=USER,
    )
    date_joined = models.DateTimeField(
            auto_now_add=True,
    )
    password = models.CharField(
            max_length=150,
            help_text='Введите пароль',
    )

    def __str__(self):
        return self.get_full_name()

    @property
    def is_moderator(self):
        return self.is_staff or self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='author')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                    fields=['user', 'author'], name='unique_follow'
            ),
            models.CheckConstraint(
                    check=~Q(user=F('author')),
                    name='self_following',
            ),
        ]

    def __str__(self):
        return f'{self.user} is following {self.author}'
