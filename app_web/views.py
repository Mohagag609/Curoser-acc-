from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from app_core import models as m
from .forms import CustomerForm

def dashboard(request):
    return render(request, 'dashboard.html')


def customers_index(request):
    return render(request, 'customers/index.html', {"title": "العملاء"})


def customers_table(request):
    q = (request.GET.get('q') or '').strip()
    qs = m.Customer.objects.all().order_by('name')
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, 'customers/_table.html', {"customers": qs})


@require_POST
def customer_create(request):
    form = CustomerForm(request.POST)
    if not form.is_valid():
        return render(request, 'customers/_form.html', {"form": form}, status=400)
    form.save()
    return customers_table(request)


def customer_edit(request, pk: int):
    customer = get_object_or_404(m.Customer, pk=pk)
    form = CustomerForm(instance=customer)
    return render(request, 'customers/_form.html', {"form": form, "obj": customer})


@require_POST
def customer_update(request, pk: int):
    customer = get_object_or_404(m.Customer, pk=pk)
    form = CustomerForm(request.POST, instance=customer)
    if not form.is_valid():
        return render(request, 'customers/_form.html', {"form": form, "obj": customer}, status=400)
    form.save()
    return customers_table(request)


@require_POST
def customer_delete(request, pk: int):
    customer = get_object_or_404(m.Customer, pk=pk)
    customer.delete()
    return customers_table(request)


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
