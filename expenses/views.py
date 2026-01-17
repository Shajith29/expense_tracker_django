from django.shortcuts import render,redirect
from .models import Expense,Category
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from django.shortcuts import get_object_or_404
from .forms import ExpenseForm,CategoryForm
from .services import filter_by_category,filter_by_month_year,search,pagination,filter_by_date
from datetime import date
from django.db.models import Sum,ProtectedError,Count
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
import calendar


# Create your views here.

@login_required
def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    
    category_id = request.GET.get("category")
    search_query = request.GET.get("q")
    month = request.GET.get("month")
    year = request.GET.get("year")
    from_date = request.GET.get("from")
    to_date = request.GET.get("to")

    #Filtering
    expenses  = filter_by_category(expenses,category_id)
    expenses = filter_by_month_year(expenses,month,year)
    expenses = search(expenses,search_query)
    expenses = filter_by_date(expenses,from_date,to_date)

    expenses = expenses.order_by('date') if from_date and to_date else expenses.order_by('-date')

    categories = Category.objects.filter(user=request.user)
    
    current_year = date.today().year

    years = range(current_year - 3,current_year + 1)

    #Pagination
    page_obj = pagination(request,expenses)

    context = {
        "expenses": page_obj.object_list,
        "page_obj": page_obj,
        "categories":categories,
        "selected_category":category_id,
        "selected_month": month,
        "selected_year":year,
        "months":range(1,13),
        "years":years,
        "search_query": search_query,
        "from_date":from_date,
        "to_date":to_date
    }

    return render(request,"expenses/list_expenses.html",context)

@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request,"Expense Added Successfully")
            return redirect("list_expenses")

    else:
        form = ExpenseForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)

    return render(request,"expenses/expense_form.html",{"form": form})

@login_required
def edit_expense(request,expense_id):
    expense = get_object_or_404(
        Expense,
        pk=expense_id,
        user=request.user
    )


    if request.method == "POST":
        form = ExpenseForm(request.POST,instance=expense)
        form.fields['category'] = Category.objects.filter(user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Expense Updated Successfully")
            return redirect("list_expenses")
    else:
        form = ExpenseForm(instance=expense)

    
    return render(request,'expenses/expense_form.html',{"form": form})

@login_required
def delete_expense(request,expense_id):
    expense = get_object_or_404(Expense,pk=expense_id,user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request,"Expense Deleted Successfully")
        return redirect("list_expenses")
    

    return render(request,"expenses/confirm_delete.html",{"expense": expense})


@login_required
def list_categories(request):
    categories = Category.objects.filter(user=request.user).annotate(expense_count=Count("expense"))

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request,"Category Created Successfully")
            return redirect('list_categories')
    
    else:
        form = CategoryForm()

    
    return render(request,'expenses/list_categories.html',{"categories": categories, "form": form})


def monthly_summary_view(request):
    today = date.today()
    month = request.GET.get('month')
    year = request.GET.get('year')

    month  = month or today.month
    year = year or today.year

    expenses = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    total_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    category_summary = (
        expenses
        .values('category__name')
        .annotate(total=Sum("amount"))
        .order_by('-total')
    )

    context = {
        "month":month,
        "year":year,
        "total_expense":total_expense,
        "category_summary":category_summary,
        "months":range(1,13),
        "years": range(today.year - 3,today.year + 1)
    }

    return render(request,'expenses/monthly_summary.html',context=context)



def delete_category(request,pk):
    category = get_object_or_404(
        Category,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        try:
            category.delete()
            messages.success(request,"Category Deleted Successfully")
        except ProtectedError:
            messages.error(request,"Cannot this Category used by  expenses")

        return redirect('list_categories')

    return render(request,"expenses/list_categories.html",{"category": category})


def export_expenses_csv(request):
    expenses = Expense.objects.filter(user=request.user)

    category_id = request.GET.get("category")
    month = request.GET.get("month")
    year = request.GET.get("year")
    search_query = request.GET.get("q")
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    #Filter Expenses

    expenses = filter_by_category(expenses,category_id)
    expenses = filter_by_month_year(expenses,month,year)
    expenses = search(expenses,search_query)
    expenses = filter_by_date(expenses,from_date,to_date)

    expenses = expenses.order_by('-date')

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Dispostion": "attachement; filename='expenses.csv'"
        }   
    )

    writer = csv.writer(response)
    writer.writerow(["Date","Category","Amount","Description"])

    for expense in expenses:
        writer.writerow([
            expense.date,
            expense.category,
            expense.amount,
            expense.description
        ])

    return response

   
def yearly_summary(request):
    year = request.GET.get("year")

    current_year = date.today().year

    year = int(year) if year else current_year

    expenses = Expense.objects.filter(
        user=request.user,
        date__year=year
    )

    monthly_summary = (
        expenses
        .values("date__month")
        .annotate(total=Sum('amount'))
        .order_by('date__month')
    )

    for row in monthly_summary:
        row["date__month"] = calendar.month_name[row["date__month"]]

    yearly_total = expenses.aggregate(total=Sum('amount'))["total"] or 0

    context = {
        "selected_year":year,
        "monthly_summary":monthly_summary,
        "yearly_total":yearly_total,
        "years": range(current_year - 3,current_year + 1)
    } 

    return render(request,"expenses/yearly_summary.html",context)
