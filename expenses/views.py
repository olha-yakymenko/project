from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncYear
from django.views.generic.list import ListView
from .forms import ExpenseSearchForm
from .models import Expense, Category
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5  # Limit the number of items per page

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)

        # Processing the search form
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

            from_date = form.cleaned_data.get('from_date')
            if from_date:
                queryset = queryset.filter(date__gte=from_date)

            to_date = form.cleaned_data.get('to_date')
            if to_date:
                queryset = queryset.filter(date__lte=to_date)

            categories = form.cleaned_data.get('categories')
            if categories:
                queryset = queryset.filter(category__in=categories)

            sort_by = form.cleaned_data.get('sort_by', 'date')
            order = form.cleaned_data.get('order', 'asc')

            if sort_by == 'date':
                queryset = queryset.order_by('date' if order == 'asc' else '-date')
            elif sort_by == 'category':
                queryset = queryset.order_by(
                    'category__name' if order == 'asc' else '-category__name'
                )

        # Calculating the total expense amount
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0

        # Creating a summary of expenses by category
        summary_per_category = queryset.values('category__name').annotate(total=Sum('amount')).order_by('category__name')

        # Creating a monthly summary
        summary_per_month = queryset.annotate(
            month=TruncMonth('date')
        ).values('month').annotate(total=Sum('amount')).order_by('month')
        
        # Creating a yearly summary by category
        summary_per_category_year = queryset.annotate(
            year=TruncYear('date')
        ).values('year', 'category__name').annotate(total=Sum('amount')).order_by('year', 'category__name')

        # Returning context to the template
        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category,
            total_amount=total_amount,
            summary_per_month=summary_per_month,
            summary_per_category_year=summary_per_category_year,
            **kwargs
        )


class CategoryListView(ListView):
    model = Category
    paginate_by = None  # Can be None if you want to display all categories

    def get_queryset(self):
        # Returns all categories with the number of expenses
        return Category.objects.annotate(expenses_count=Count('expense'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding categories with the number of expenses
        context['categories_with_expenses'] = context['object_list']
        return context


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']  # Only the 'name' field can be edited
    template_name = 'expenses/category_form.html'  
    success_url = reverse_lazy('expenses:category-list')
