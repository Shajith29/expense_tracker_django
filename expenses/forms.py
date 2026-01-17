from django import forms
from .models import Expense,Category


class TailwindFormMixin:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():
            classes = "w-full border px-3 py-2 rounded"

            if self.errors.get(name):
                classes += " border-red-500"
            else:
                classes += " border-gray-300"

            field.widget.attrs["class"] = classes

class ExpenseForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category','amount','description','date']
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'})
        }


class CategoryForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name',]