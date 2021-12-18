from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from rest_framework_simplejwt.token_blacklist import admin as TokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from .forms import UserChangeForm, UserCreationForm
from .models import Profile, User


class OutstandingTokenAdmin(TokenAdmin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_admin', 'is_superuser', 'premium', 'premium_expiration_date', 'premium_life', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'premium', 'is_course_creator')
    list_filter = ('is_admin', 'is_superuser', 'premium', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_field = ['user']


admin.site.unregister(Group)
admin.site.unregister(OutstandingToken)


admin.site.register(User, UserAdmin)
admin.site.register(OutstandingToken, OutstandingTokenAdmin)
admin.site.register(Profile, ProfileAdmin)