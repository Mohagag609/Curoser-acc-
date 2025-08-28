from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from app_core import models as m
from .forms import CustomerForm, UnitForm, ContractForm

def dashboard(request):
    return render(request, 'dashboard.html')


def customers_index(request):
    return render(request, 'customers/index.html', {"title": "العملاء"})


def customer_form(request):
    form = CustomerForm()
    return render(request, 'customers/_form.html', {"form": form})


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
    return render(request, 'units/index.html', {"title": "الوحدات"})


def unit_form(request):
    form = UnitForm()
    return render(request, 'units/_form.html', {"form": form})


def units_table(request):
    q = (request.GET.get('q') or '').strip()
    qs = m.Unit.objects.all().order_by('code')
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q)
    return render(request, 'units/_table.html', {"units": qs})


@require_POST
def unit_create(request):
    form = UnitForm(request.POST)
    if form.is_valid():
        unit = form.save(commit=False)
        if not unit.code:
            # توليد كود مبسط عند عدم إدخاله
            base = (unit.building or '').replace(' ', '')
            floor = (unit.floor or '').replace(' ', '')
            name = (unit.name or '').replace(' ', '')
            unit.code = f"{base}-{floor}-{name}" or "U-" + str(m.Unit.objects.count() + 1)
        unit.save()
        return units_table(request)
    return render(request, 'units/_form.html', {"form": form}, status=400)


def unit_edit(request, pk: int):
    unit = get_object_or_404(m.Unit, pk=pk)
    form = UnitForm(instance=unit)
    return render(request, 'units/_form.html', {"form": form, "obj": unit})


@require_POST
def unit_update(request, pk: int):
    unit = get_object_or_404(m.Unit, pk=pk)
    form = UnitForm(request.POST, instance=unit)
    if form.is_valid():
        unit = form.save()
        return units_table(request)
    return render(request, 'units/_form.html', {"form": form, "obj": unit}, status=400)


@require_POST
def unit_delete(request, pk: int):
    unit = get_object_or_404(m.Unit, pk=pk)
    unit.delete()
    return units_table(request)


def contracts_index(request):
    return render(request, 'contracts/index.html', {"title": "العقود"})


def contracts_table(request):
    qs = m.Contract.objects.select_related('unit', 'customer').order_by('-created_at')
    return render(request, 'contracts/_table.html', {"contracts": qs})


def contract_form(request):
    form = ContractForm()
    return render(request, 'contracts/_form.html', {"form": form})


@require_POST
def contract_create(request):
    form = ContractForm(request.POST)
    if not form.is_valid():
        return render(request, 'contracts/_form.html', {"form": form}, status=400)
    ct: m.Contract = form.save(commit=False)
    # code generation
    next_num = m.Contract.objects.count() + 1
    ct.code = f"CTR-{next_num:05d}"
    ct.save()
    # schedule installments (simplified, monthly)
    if ct.payment_type == 'installment':
        from datetime import date
        from dateutil.relativedelta import relativedelta
        total_after_down = (ct.total_price - ct.discount_amount - ct.down_payment - ct.maintenance_deposit)
        total_after_down = max(total_after_down, 0)
        extra_total = (ct.extra_annual or 0) * (ct.annual_payment_value or 0)
        amount_for_regular = max(total_after_down - extra_total, 0)
        months_map = {"شهري": 1, "ربع سنوي": 3, "نصف سنوي": 6, "سنوي": 12}
        step = months_map.get(ct.schedule_type or 'شهري', 1)
        count = ct.count or 0
        # regular installments
        if count > 0:
            base = (amount_for_regular / count) if count else 0
            acc = 0
            for i in range(count):
                due = ct.start + relativedelta(months=step * (i + 1))
                amount = round(base, 2)
                if i == count - 1:
                    amount = round(amount_for_regular - acc, 2)
                m.Installment.objects.create(
                    unit=ct.unit,
                    type=ct.schedule_type or 'شهري',
                    original_amount=amount,
                    amount_remaining=amount,
                    due_date=due,
                    status='غير مدفوع',
                )
                acc += amount
        # annual extras
        for j in range(ct.extra_annual or 0):
            due = ct.start + relativedelta(months=12 * (j + 1))
            val = ct.annual_payment_value or 0
            if val > 0:
                m.Installment.objects.create(
                    unit=ct.unit,
                    type='دفعة سنوية',
                    original_amount=val,
                    amount_remaining=val,
                    due_date=due,
                    status='غير مدفوع',
                )
        # maintenance deposit after last installment
        if ct.maintenance_deposit and ct.maintenance_deposit > 0:
            last = m.Installment.objects.filter(unit=ct.unit).order_by('-due_date').first()
            from datetime import timedelta
            due = (last.due_date if last else ct.start) + relativedelta(months=step)
            m.Installment.objects.create(
                unit=ct.unit,
                type='دفعة صيانة',
                original_amount=ct.maintenance_deposit,
                amount_remaining=ct.maintenance_deposit,
                due_date=due,
                status='غير مدفوع',
            )
        # mark unit sold
        ct.unit.status = 'مباعة'
        ct.unit.save(update_fields=['status'])
    return contracts_table(request)


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
