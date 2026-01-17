from django.urls import path
from . import views

urlpatterns = [
    path('',views.list_expenses,name='list_expenses'),
    path('create/',views.create_expense,name='create_expense'),
    path('<int:expense_id>/edit/',views.edit_expense,name='edit_expense'),
    path('<int:expense_id>/delete/',views.delete_expense,name = "delete_expense"),

    path('categories/',views.list_categories,name= "list_categories"),
    path("categories/<int:pk>/delete",views.delete_category, name = "delete_category"),
    path('summary/',views.monthly_summary_view,name= "monthly_summary"),
    path('summary/yearly',views.yearly_summary,name="yearly_summary"),

    path('/export/csv',views.export_expenses_csv,name="export_expenses_csv")

]