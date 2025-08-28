from django.shortcuts import render


def dashboard(request):
    return render(request, 'dashboard.html')


def customers_index(request):
    return render(request, 'scaffold/list.html', {"title": "العملاء"})


def units_index(request):
    return render(request, 'scaffold/list.html', {"title": "الوحدات"})


def contracts_index(request):
    return render(request, 'scaffold/list.html', {"title": "العقود"})


def vouchers_index(request):
    return render(request, 'scaffold/list.html', {"title": "السندات"})


def partners_index(request):
    return render(request, 'scaffold/list.html', {"title": "الشركاء"})


def treasury_index(request):
    return render(request, 'scaffold/list.html', {"title": "الخزينة"})


def reports_index(request):
    return render(request, 'scaffold/list.html', {"title": "التقارير"})
from django.shortcuts import render

# Create your views here.
