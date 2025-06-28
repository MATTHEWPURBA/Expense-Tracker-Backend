from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'type', 'category', 'user', 'date', 'created_at']
    list_filter = ['type', 'category', 'date', 'created_at']
    search_fields = ['title', 'description', 'user__username', 'category__name']
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'amount', 'type', 'category', 'user', 'date')
        }),
        ('Additional', {
            'fields': ('receipt', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'category')

# apps/transactions/admin.py