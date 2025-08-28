from django.contrib import admin
from . import models as m


@admin.register(m.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "national_id", "status")
    search_fields = ("name", "phone", "national_id")


@admin.register(m.Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "building", "floor", "status", "total_price")
    list_filter = ("status",)
    search_fields = ("code", "name", "building", "floor")


@admin.register(m.Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


@admin.register(m.UnitPartner)
class UnitPartnerAdmin(admin.ModelAdmin):
    list_display = ("unit", "partner", "percent")
    list_filter = ("unit", "partner")


@admin.register(m.PartnerGroup)
class PartnerGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(m.PartnerGroupMember)
class PartnerGroupMemberAdmin(admin.ModelAdmin):
    list_display = ("group", "partner", "percent")
    list_filter = ("group",)


@admin.register(m.Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


@admin.register(m.Safe)
class SafeAdmin(admin.ModelAdmin):
    list_display = ("name", "balance")
    search_fields = ("name",)


@admin.register(m.Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("code", "unit", "customer", "total_price", "start")
    search_fields = ("code",)
    list_filter = ("payment_type",)


@admin.register(m.Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ("unit", "type", "original_amount", "amount_remaining", "due_date", "status")
    list_filter = ("status", "due_date")


@admin.register(m.BrokerDue)
class BrokerDueAdmin(admin.ModelAdmin):
    list_display = ("contract", "broker_name", "amount", "status", "due_date")
    list_filter = ("status", "due_date")


@admin.register(m.Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ("date", "type", "amount", "safe", "description")
    list_filter = ("type", "date", "safe")
    search_fields = ("description",)


@admin.register(m.PartnerDebt)
class PartnerDebtAdmin(admin.ModelAdmin):
    list_display = ("unit", "paying_partner", "owed_partner", "amount", "due_date", "status")
    list_filter = ("status", "due_date")


@admin.register(m.Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("from_safe", "to_safe", "amount", "date")


@admin.register(m.SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "theme", "font_px")


@admin.register(m.AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "description")
    search_fields = ("description",)
from django.contrib import admin

# Register your models here.
