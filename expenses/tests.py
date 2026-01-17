from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category,Expense
from datetime import date
from django.urls import reverse

# Create your tests here.

class ExpenseBaseTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="pass123"
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="pass123"
        )

        self.cat_food_u1 = Category.objects.create(
            name='Food',
            user=self.user1
        )

        self.cat_travel_u2  = Category.objects.create(
            name="Travel",
            user=self.user2
        )

        self.u1_expense = Expense.objects.create(
            user=self.user1,
            category=self.cat_food_u1,
            description="Lunch",
            amount=140,
            date=date(2026,1,13)
        )

        self.u2_expense = Expense.objects.create(
            user=self.user2,
            category=self.cat_travel_u2,
            amount=40,
            description='Bus',
            date=date(2026,1,13)
        )


class ExpensesPermissionTests(ExpenseBaseTest):

    def test_user_can_list_only_thier_expenses(self):
        self.client.login(username="user1",password="pass123")

        response = self.client.get(reverse('list_expenses'))

        expenses = response.context['expenses']

        self.assertEqual(len(expenses),1)
        self.assertEqual(expenses[0].user,self.user1)

    def test_other_user_cannot_edit_other_users_expenses(self):
        self.client.login(username="user1",password="pass123")

        response = self.client.get(reverse('edit_expense',args=[self.u2_expense.id]))

        self.assertEqual(response.status_code,404)

    def test_anonymous_users_are_redirected(self):
        response = self.client.get(reverse('list_expenses'))

        self.assertEqual(response.status_code,302)


class ExpenseLogicTest(ExpenseBaseTest):
    def test_expense_creation(self):
        self.client.login(username="user1",password="pass123")

        response = self.client.post(reverse('create_expense'),{
            "category":self.cat_food_u1.pk,
            "amount":100,
            "description": "Dinner",
            "date":"2026-1-13"
        })

        self.assertEqual(Expense.objects.filter(user=self.user1).count(),2)
        self.assertEqual(response.status_code,302)

    def test_category_filtering(self):
        self.client.login(username="user1",password="pass123")

        response = self.client.get(reverse("list_expenses"),{
            "category":self.cat_food_u1.pk
        })

        expenses = response.context['expenses']

        self.assertEqual(len(expenses),1)
        self.assertEqual(expenses[0].user,self.user1)

    def test_monthly_expense_total(self):
        self.client.login(username="user1",password="pass123")

        response = self.client.get(reverse('monthly_summary'),{
            "month":1,
            "year":2026
        })

        self.assertEqual(response.context['total_expense'],140)