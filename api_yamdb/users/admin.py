from django.contrib.admin import ModelAdmin, register

from users.models import User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'username', 'role')
    empty_value_display = '---'
