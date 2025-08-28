from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError

from app_core import models as m


class CustomerForm(forms.ModelForm):
    class Meta:
        model = m.Customer
        fields = ["name", "phone", "national_id", "address", "status", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "phone": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "national_id": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "address": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "status": forms.TextInput(attrs={"class": "w-full border rounded px-3 py-2"}),
            "notes": forms.Textarea(attrs={"rows": 2, "class": "w-full border rounded px-3 py-2"}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = m.Unit
        fields = ["code", "name", "floor", "building", "unit_type", "area", "total_price", "status", "notes"]


class PartnerForm(forms.ModelForm):
    class Meta:
        model = m.Partner
        fields = ["name", "phone"]


class PartnerGroupForm(forms.ModelForm):
    class Meta:
        model = m.PartnerGroup
        fields = ["name"]


class PartnerGroupMemberForm(forms.ModelForm):
    class Meta:
        model = m.PartnerGroupMember
        fields = ["partner", "percent"]


class BrokerForm(forms.ModelForm):
    class Meta:
        model = m.Broker
        fields = ["name", "phone", "notes"]


class SafeForm(forms.ModelForm):
    class Meta:
        model = m.Safe
        fields = ["name", "balance"]


class TransferForm(forms.ModelForm):
    class Meta:
        model = m.Transfer
        fields = ["from_safe", "to_safe", "amount", "date", "notes"]

    def clean(self):
        cleaned = super().clean()
        from_safe = cleaned.get("from_safe")
        to_safe = cleaned.get("to_safe")
        amount = cleaned.get("amount")
        if from_safe and to_safe and from_safe == to_safe:
            raise ValidationError("لا يمكن التحويل لنفس الخزنة")
        if amount is not None and amount <= 0:
            raise ValidationError("أدخل مبلغًا صحيحًا")
        return cleaned


class ExpenseVoucherForm(forms.Form):
    description = forms.CharField(max_length=255)
    beneficiary = forms.CharField(max_length=255, required=False)
    amount = forms.DecimalField(max_digits=14, decimal_places=2)
    date = forms.DateField()
    safe = forms.ModelChoiceField(queryset=m.Safe.objects.all())


SCHEDULE_TYPES = (
    ("شهري", "شهري"),
    ("ربع سنوي", "ربع سنوي"),
    ("نصف سنوي", "نصف سنوي"),
    ("سنوي", "سنوي"),
)


class ContractForm(forms.ModelForm):
    payment_type = forms.ChoiceField(choices=(("installment", "تقسيط"), ("cash", "كاش")))
    schedule_type = forms.ChoiceField(choices=SCHEDULE_TYPES, required=False)
    count = forms.IntegerField(min_value=0, required=False, initial=0)
    extra_annual = forms.IntegerField(min_value=0, required=False, initial=0)
    annual_payment_value = forms.DecimalField(max_digits=14, decimal_places=2, required=False, initial=0)
    start = forms.DateField()

    class Meta:
        model = m.Contract
        fields = [
            "unit",
            "customer",
            "total_price",
            "down_payment",
            "discount_amount",
            "maintenance_deposit",
            "payment_type",
            "schedule_type",
            "count",
            "extra_annual",
            "annual_payment_value",
            "start",
            "broker_name",
            "broker_percent",
            "commission_safe",
        ]

    def clean(self):
        cleaned = super().clean()
        unit: m.Unit | None = cleaned.get("unit")
        if unit and unit.status == "مباعة":
            raise ValidationError("لا يمكن إنشاء عقد لوحدة مباعة")
        return cleaned
