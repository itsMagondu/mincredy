"""url module for routing requests
"""
from django.urls import path
from api.v1.users.views import all_users, manage_user, all_loans, manage_loan
app_name = 'users'


urlpatterns = [
    path('users/', all_users, name="get_users"),
    path('users/<int:id>/', manage_user, name="manage_user"),
    path('loans/', all_loans, name="get_loans"),
    path('loans/<int:id>/', manage_loan, name="manage_loan"),
]
