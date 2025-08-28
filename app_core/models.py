from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=64, blank=True, default="")
    national_id = models.CharField(max_length=64, blank=True, default="")
    address = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=32, blank=True, default="نشط")
    notes = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["national_id"]),
        ]

    def __str__(self) -> str:
        return self.name


class Unit(TimeStampedModel):
    STATUS_CHOICES = (
        ("متاحة", "متاحة"),
        ("محجوزة", "محجوزة"),
        ("مباعة", "مباعة"),
        ("مرتجعة", "مرتجعة"),
    )
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    floor = models.CharField(max_length=64, blank=True, default="")
    building = models.CharField(max_length=64, blank=True, default="")
    unit_type = models.CharField(max_length=64, blank=True, default="سكني")
    area = models.CharField(max_length=64, blank=True, default="")
    total_price = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="متاحة")
    notes = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["status"]),
            models.Index(fields=["building", "floor", "name"]),
        ]

    def __str__(self) -> str:
        base = self.name or ""
        parts = [p for p in [base, self.floor, self.building] if p]
        return self.code if self.code else " ".join(parts)


class Partner(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=64, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class UnitPartner(TimeStampedModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="unit_partners")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="unit_partners")
    percent = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("unit", "partner")

    def __str__(self) -> str:
        return f"{self.unit_id}-{self.partner_id} {self.percent}%"


class PartnerGroup(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class PartnerGroupMember(TimeStampedModel):
    group = models.ForeignKey(PartnerGroup, on_delete=models.CASCADE, related_name="members")
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    percent = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ("group", "partner")


class Broker(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=64, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return self.name


class Safe(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.name


class Contract(TimeStampedModel):
    PAYMENT_TYPE = (
        ("installment", "installment"),
        ("cash", "cash"),
    )
    code = models.CharField(max_length=64, unique=True)
    unit = models.OneToOneField(Unit, on_delete=models.PROTECT, related_name="contract")
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="contracts")
    total_price = models.DecimalField(max_digits=14, decimal_places=2)
    down_payment = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    maintenance_deposit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    payment_type = models.CharField(max_length=16, choices=PAYMENT_TYPE, default="installment")
    schedule_type = models.CharField(max_length=32, blank=True, default="شهري")
    count = models.IntegerField(default=0)
    extra_annual = models.IntegerField(default=0)
    annual_payment_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    start = models.DateField()
    broker_name = models.CharField(max_length=255, blank=True, default="")
    broker_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    broker_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    commission_safe = models.ForeignKey(Safe, on_delete=models.SET_NULL, null=True, blank=True, related_name="commission_contracts")

    def __str__(self) -> str:
        return self.code


class Installment(TimeStampedModel):
    STATUS_CHOICES = (
        ("غير مدفوع", "غير مدفوع"),
        ("مدفوع جزئياً", "مدفوع جزئياً"),
        ("مدفوع", "مدفوع"),
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="installments")
    type = models.CharField(max_length=64)
    original_amount = models.DecimalField(max_digits=14, decimal_places=2)
    amount_remaining = models.DecimalField(max_digits=14, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="غير مدفوع")

    class Meta:
        indexes = [
            models.Index(fields=["unit", "due_date"]),
            models.Index(fields=["status"]),
        ]


class BrokerDue(TimeStampedModel):
    STATUS = (("due", "due"), ("paid", "paid"))
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="broker_dues")
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True, blank=True)
    broker_name = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=8, choices=STATUS, default="due")
    payment_date = models.DateField(null=True, blank=True)
    paid_from_safe = models.ForeignKey(Safe, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["status", "due_date"])]


class Voucher(TimeStampedModel):
    TYPE = (("receipt", "receipt"), ("payment", "payment"))
    type = models.CharField(max_length=8, choices=TYPE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    safe = models.ForeignKey(Safe, on_delete=models.PROTECT, related_name="vouchers")
    description = models.TextField(blank=True, default="")
    payer = models.CharField(max_length=255, blank=True, default="")
    beneficiary = models.CharField(max_length=255, blank=True, default="")
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True, related_name="vouchers")
    installment = models.ForeignKey(Installment, on_delete=models.SET_NULL, null=True, blank=True, related_name="vouchers")
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name="vouchers")
    broker_due = models.ForeignKey(BrokerDue, on_delete=models.SET_NULL, null=True, blank=True, related_name="vouchers")
    raw_linked_ref = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["type"]),
        ]


class PartnerDebt(TimeStampedModel):
    STATUS = (("غير مدفوع", "غير مدفوع"), ("مدفوع", "مدفوع"))
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="partner_debts")
    paying_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="debts_to_pay")
    owed_partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="debts_to_collect")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=16, choices=STATUS, default="غير مدفوع")
    payment_date = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["status", "due_date"])]


class Transfer(TimeStampedModel):
    from_safe = models.ForeignKey(Safe, on_delete=models.PROTECT, related_name="transfers_from")
    to_safe = models.ForeignKey(Safe, on_delete=models.PROTECT, related_name="transfers_to")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, default="")


class SiteSettings(models.Model):
    THEME = (("dark", "dark"), ("light", "light"))
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    theme = models.CharField(max_length=8, choices=THEME, default="dark")
    font_px = models.PositiveIntegerField(default=16)
    lock_pin = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self) -> str:
        return f"Settings#{self.pk}"


class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    details = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self) -> str:
        return f"{self.timestamp} {self.description}"

from django.db import models

# Create your models here.
