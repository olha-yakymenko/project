from django import forms
from .models import Expense, Category

class ExpenseSearchForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name',)

    from_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label='Start Date'
    )

    to_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label='End Date'
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), 
        required=False, 
        label='Categories'
    )

    sort_by = forms.ChoiceField(
        choices=[('date', 'Date'), ('category', 'Category')], 
        required=False, 
        initial='date',
        label='Sort by'
    )

    order = forms.ChoiceField(
        choices=[('asc', 'Ascending'), ('desc', 'Descending')], 
        required=False, 
        initial='asc',
        label='Order'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
