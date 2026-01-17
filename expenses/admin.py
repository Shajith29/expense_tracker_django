from django.contrib import admin
from .models import Category,Expense


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','user','created_at')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user','category','amount','date','created_at')
    list_filter = ('category','date')
    search_fields = ('description',)


