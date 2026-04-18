from django.contrib import admin
from .models import Client, Invoice, InvoiceItem, Payment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'company_name', 'email']
    list_filter = ['created_at']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'client', 'date_issued', 'due_date', 'status', 'grand_total', 'currency']
    list_filter = ['status', 'date_issued', 'due_date']
    search_fields = ['invoice_number', 'client__name']
    readonly_fields = ['subtotal', 'tax_amount', 'grand_total', 'public_token']
    inlines = [InvoiceItemInline, PaymentInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('client')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['service_category', 'quantity', 'unit_price', 'total', 'invoice']
    search_fields = ['service_category', 'invoice__invoice_number']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'method', 'reference', 'created_at']
    list_filter = ['method', 'created_at']
    search_fields = ['invoice__invoice_number', 'reference']
