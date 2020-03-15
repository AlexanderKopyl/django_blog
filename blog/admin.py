from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Post, UserProfile

admin.site.register(Post)


class ProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('avatar_tag', 'avatar',)
    readonly_fields = ['avatar_tag']
    fk_name = 'user'
    max_num = 1


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline, ]

    # модифицируем список отображаемых полей, чтобы увидеть аватарку с остальными полями
    list_display = ('avatar_tag',) + UserAdmin.list_display

    # а также создаём метод для получения тега аватарки из пользовательского профиля
    def avatar_tag(self, obj):
        return obj.userprofile.avatar_tag()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
