from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet

# We'll define the URLS manually to be extra flexible with trailing slashes
expense_list = ExpenseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
expense_detail = ExpenseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
expense_summary = ExpenseViewSet.as_view({
    'get': 'summary'
})
expense_convert = ExpenseViewSet.as_view({
    'get': 'convert_currency'
})

urlpatterns = [
    # Match with or without trailing slash
    path('expenses', expense_list, name='expense-list'),
    path('expenses/', expense_list, name='expense-list-slash'),
    path('expenses/summary', expense_summary, name='expense-summary'),
    path('expenses/summary/', expense_summary, name='expense-summary-slash'),
    path('expenses/convert_currency', expense_convert, name='expense-convert'),
    path('expenses/convert_currency/', expense_convert, name='expense-convert-slash'),
    path('expenses/<int:pk>', expense_detail, name='expense-detail'),
    path('expenses/<int:pk>/', expense_detail, name='expense-detail-slash'),
]
