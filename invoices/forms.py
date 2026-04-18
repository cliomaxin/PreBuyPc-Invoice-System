from django import forms
from django.forms import modelformset_factory
from .models import Client, Invoice, InvoiceItem, Payment


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'company_name', 'billing_address', 'kra_pin', 'notes']
        widgets = {
            'billing_address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'currency', 'date_issued', 'due_date', 'status', 'tax_rate', 'discount', 'notes']
        widgets = {
            'date_issued': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['service_category', 'detail_notes', 'quantity', 'unit_price']
        widgets = {
            'detail_notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields not required
        self.fields['service_category'].required = False
        self.fields['quantity'].required = False
        self.fields['unit_price'].required = False
        # Set initial values
        self.fields['quantity'].initial = 0
        self.fields['unit_price'].initial = 0


# Formset for invoice items
InvoiceItemFormSet = modelformset_factory(
    InvoiceItem,
    form=InvoiceItemForm,
    extra=0,
    can_delete=True
)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'method', 'reference', 'phone']
        widgets = {
            'reference': forms.TextInput(attrs={'placeholder': 'M-Pesa transaction ID'}),
        }