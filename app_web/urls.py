from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customers_index, name='customers_index'),
    path('units/', views.units_index, name='units_index'),
    path('contracts/', views.contracts_index, name='contracts_index'),
    path('vouchers/', views.vouchers_index, name='vouchers_index'),
    path('partners/', views.partners_index, name='partners_index'),
    path('treasury/', views.treasury_index, name='treasury_index'),
    path('reports/', views.reports_index, name='reports_index'),
]
