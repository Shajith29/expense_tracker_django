from .models import Expense
from django.core.paginator import Paginator

def filter_by_category(query_set,category_id):

    if category_id in ["","None",None]:
        category_id = None

    if category_id:
        return query_set.filter(category_id=category_id)
    return query_set


def filter_by_month_year(query_set,month,year):

    if not month or year:
        month = year = None
    
    if month and year:
        return query_set.filter(
            date__month = month,
            date__year = year
        )
    
    return query_set

def search(queryset,search_query):
    if search_query:
        return queryset.filter(description__icontains=search_query)
    
    return queryset


def pagination(request,queryset):
    paginator = Paginator(queryset,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return page_obj

def filter_by_date(queryset,from_date,to_date):
    if from_date and to_date:
        return queryset.filter(
            date__gte=from_date,
            date__lte=to_date
        )
    return queryset



    

    
