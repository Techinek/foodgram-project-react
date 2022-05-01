from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email',
                    'role')
    list_filter = ('username', 'email')
    search_fields = ('username',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('author',)


admin.site.register(Follow, FollowAdmin)
admin.site.register(User, UserAdmin)
