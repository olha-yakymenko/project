from django.contrib import admin
from .models import Category, Expense

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'expense_count')  # Display category name and number of expenses
    search_fields = ('name',)

    def expense_count(self, obj):
        return obj.expense_set.count()  # Count the number of expenses for each category
    expense_count.short_description = 'Number of Expenses'


# Register the Expense model
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'amount', 'date')  # Display relevant fields
    list_filter = ('category', 'date')  # Filter by category and date
    search_fields = ('name', 'category__name')  # Search by name and category name
    ordering = ('-date',)  # Order by date descending
