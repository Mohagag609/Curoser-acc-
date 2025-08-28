from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customers_index, name='customers_index'),
    path('customers/form/', views.customer_form, name='customer_form'),
    path('customers/table/', views.customers_table, name='customers_table'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('units/', views.units_index, name='units_index'),
    path('units/form/', views.unit_form, name='unit_form'),
    path('units/table/', views.units_table, name='units_table'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:pk>/edit/', views.unit_edit, name='unit_edit'),
    path('units/<int:pk>/update/', views.unit_update, name='unit_update'),
    path('units/<int:pk>/delete/', views.unit_delete, name='unit_delete'),
    path('contracts/', views.contracts_index, name='contracts_index'),
    path('contracts/table/', views.contracts_table, name='contracts_table'),
    path('contracts/form/', views.contract_form, name='contract_form'),
    path('contracts/create/', views.contract_create, name='contract_create'),
    path('vouchers/', views.vouchers_index, name='vouchers_index'),
    path('partners/', views.partners_index, name='partners_index'),
    path('treasury/', views.treasury_index, name='treasury_index'),
    path('reports/', views.reports_index, name='reports_index'),
    # installments
    path('installments/', views.installments_index, name='installments_index'),
    path('installments/table/', views.installments_table, name='installments_table'),
    path('installments/<int:pk>/pay/', views.installment_pay, name='installment_pay'),
    # vouchers
    path('vouchers/table/', views.vouchers_table, name='vouchers_table'),
    # safes
    path('treasury/table/', views.safes_table, name='safes_table'),
    path('treasury/create/', views.safe_create, name='safe_create'),
]
