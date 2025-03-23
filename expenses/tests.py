from django.test import TestCase
from django.urls import reverse
from .models import Expense, Category

class ExpenseListViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")
        self.expense1 = Expense.objects.create(name="Lunch", amount=15.00, date="2025-03-10", category=self.category)
        self.expense2 = Expense.objects.create(name="Dinner", amount=20.00, date="2025-03-15", category=self.category)

    def test_search_by_date_from(self):
        response = self.client.get(reverse('expenses:expense-list'), {'from_date': '2025-03-12'})
        self.assertContains(response, 'Dinner')
        self.assertNotContains(response, 'Lunch')

    def test_search_by_date_to(self):
        response = self.client.get(reverse('expenses:expense-list'), {'to_date': '2025-03-12'})
        self.assertContains(response, 'Lunch')
        self.assertNotContains(response, 'Dinner')

    def test_search_by_date_range(self):
        response = self.client.get(reverse('expenses:expense-list'), {'from_date': '2025-03-10', 'to_date': '2025-03-12'})
        self.assertContains(response, 'Lunch')
        self.assertNotContains(response, 'Dinner')

    def test_search_by_multiple_categories(self):
        expense3 = Expense.objects.create(name="Apple", amount=5.00, date="2025-03-17", category=self.category)
        response = self.client.get(reverse('expenses:expense-list'), {'categories': [self.category.id]})
        self.assertContains(response, 'Lunch')
        self.assertContains(response, 'Dinner')
        self.assertContains(response, 'Apple')

    def test_sort_by_date_ascending(self):
        response = self.client.get(reverse('expenses:expense-list'), {'sort_by': 'date', 'order': 'asc'})
        self.assertContains(response, 'Lunch')
        self.assertContains(response, 'Dinner')

    def test_sort_by_category_descending(self):
        response = self.client.get(reverse('expenses:expense-list'), {'sort_by': 'category', 'order': 'desc'})
        self.assertContains(response, 'Dinner')
        self.assertContains(response, 'Lunch')

    def test_total_amount_spent(self):
        response = self.client.get(reverse('expenses:expense-list'))
        self.assertContains(response, "35.00")  

    def test_summary_per_month(self):
        response = self.client.get(reverse('expenses:expense-list'))
        self.assertContains(response, '2025-03')  
        self.assertContains(response, "35.00")  


class CategoryUpdateViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Food")

    def test_category_update(self):
        response = self.client.post(reverse('expenses:category-edit', args=[self.category.id]), {'name': 'Updated Food'})
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Food')


class CategoryListViewTests(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Food")
        self.category2 = Category.objects.create(name="Travel")
        Expense.objects.create(name="Lunch", amount=15.00, date="2025-03-10", category=self.category1)
        Expense.objects.create(name="Flight", amount=200.00, date="2025-03-12", category=self.category2)

    def test_expenses_count_in_category_list(self):
        response = self.client.get(reverse('expenses:category-list'))
        self.assertContains(response, "<td>Food</td>", html=True)
        self.assertContains(response, "<td>1</td>", html=True)

