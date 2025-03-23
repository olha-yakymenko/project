from collections import OrderedDict
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


def summary_per_category(queryset):

    category_summary = queryset.annotate(
        category_name=Coalesce('category__name', Value('-'))  
    ).values('category_name').annotate(
        total_amount=Sum('amount') 
    ).order_by('category_name')  

    return OrderedDict((entry['category_name'], entry['total_amount']) for entry in category_summary)
