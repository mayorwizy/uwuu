from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Account, Dues, Month, Year, Position, LGA, UserProfile
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('reg_number', 'first_name', 'last_name',
                    'email', 'username', 'last_login', 'date_joined', 'is_active', )
    list_display_links = ('email', 'first_name', 'last_name', )
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    search_fields = ('email', 'username', 'first_name',
                     'last_name', 'reg_number',)

    fieldsets = (
        ('Basic Info', {'fields': ('email', 'username', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        # ('Personal', {'fields': ('about',)}),
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class MonthAdmin(admin.ModelAdmin):
    readonly_fields = ('month',)


class YearAdmin(admin.ModelAdmin):
    readonly_fields = ('year',)


class PositionAdmin(admin.ModelAdmin):
    pass


class LGAAdmin(admin.ModelAdmin):
    ordering = ('lga',)
    readonly_fields = ('lga',)


class DuesAdmin(admin.ModelAdmin):
    list_display = ('account_holder', 'amount', 'month', 'year', 'date')
    list_filter = ('year', 'month', 'amount')
    search_fields = ('account_holder__first_name',
                     'account_holder__last_name',)
    ordering = ('-date',)
    # readonly_fields = ('account_holder', 'amount', 'month', 'year', 'date')


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_pic.url))
    thumbnail.short_description = 'profile image'
    list_display = ('thumbnail', 'user', 'gender', 'dob', 'marital_status',
                    'position', 'occupation', 'lga', 'address')


admin.site.register(Account, AccountAdmin)

admin.site.register(Dues, DuesAdmin)

admin.site.register(Month, MonthAdmin)

admin.site.register(Year, YearAdmin)

admin.site.register(Position, PositionAdmin)

admin.site.register(LGA, LGAAdmin)

admin.site.register(UserProfile, UserProfileAdmin)
