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
        (ADMIN, 'admin')
    }
    email = models.EmailField(verbose_name='email address', max_length=254,
                              unique=True,
                              error_messages={'unique': 'Choose another!'})
    username = models.CharField(verbose_name='username', max_length=150,
                                unique=True,
                                error_messages={'unique': 'Choose another!'})
    first_name = models.CharField(verbose_name='first name', max_length=150,
                                  blank=True)
    last_name = models.CharField(verbose_name='last name', max_length=150,
                                 blank=True)
    role = models.CharField(verbose_name='user role', max_length=20,
                            choices=ROLES, default=USER)
    date_joined = models.DateTimeField(verbose_name='registration date',
                                       auto_now_add=True)
    password = models.CharField(verbose_name='password', max_length=150)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_full_name()

    @property
    def is_moderator(self):
        return self.is_staff or self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='user',
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(CustomUser, verbose_name='author',
                               on_delete=models.CASCADE,
                               related_name='author')

    class Meta:
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='self_following')
        ]

    def __str__(self):
        return f'{self.user} is following {self.author}'
