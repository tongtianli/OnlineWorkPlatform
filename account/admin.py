from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, WorkGroup


class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'workgroups')}),
        ('Personal info', {'fields': ('nickname', 'name', 'avatar')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(WorkGroup, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
