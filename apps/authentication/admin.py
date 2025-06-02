from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_currency', 'get_monthly_budget')
    list_filter = BaseUserAdmin.list_filter + ('profile__currency',)
    
    def get_currency(self, obj):
        return obj.profile.currency if hasattr(obj, 'profile') else None
    get_currency.short_description = 'Currency'
    
    def get_monthly_budget(self, obj):
        return obj.profile.monthly_budget if hasattr(obj, 'profile') else None
    get_monthly_budget.short_description = 'Monthly Budget'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'monthly_budget', 'phone_number', 'created_at')
    list_filter = ('currency', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Settings', {
            'fields': ('currency', 'monthly_budget', 'avatar', 'phone_number', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# apps/authentication/admin.py