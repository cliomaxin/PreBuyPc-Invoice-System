from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.urls import reverse
from .models import Client, Invoice, InvoiceItem, Payment
from .forms import InvoiceForm, InvoiceItemFormSet, PaymentForm, ClientForm
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.http import HttpResponse


def invoice_list(request):
    """List all invoices"""
    invoices = Invoice.objects.select_related('client').all()
    return render(request, 'invoices/invoice_list.html', {
        'invoices': invoices
    })


def invoice_detail(request, pk):
    """View invoice details (admin view)"""
    invoice = get_object_or_404(
        Invoice.objects.select_related('client').prefetch_related('items', 'payments'),
        pk=pk
    )
    return render(request, 'invoices/invoice_detail.html', {
        'invoice': invoice
    })


def invoice_public(request, token):
    """Public invoice view via token"""
    invoice = get_object_or_404(
        Invoice.objects.select_related('client').prefetch_related('items', 'payments'),
        public_token=token, is_active=True
    )

    # Mock business data for template
    business = {
        'name': 'PreBuyPc',
        'email': 'maxipytech@gmail.com',
        'logo': '/static/prebuypc%20logo%20rounded.png',
        'terms': None,
        'owner_name': 'Authorised Signatory'
    }

    return render(request, 'Invoice/invoice_detail.html', {
        'invoice': invoice,
        'business': business
    })


def invoice_pdf(request, token):
    """Generate PDF for public invoice"""
    from xhtml2pdf import pisa

    invoice = get_object_or_404(
        Invoice.objects.select_related('client').prefetch_related('items', 'payments'),
        public_token=token, is_active=True
    )

    # Mock business data for template
    business = {
        'name': 'PreBuyPc',
        'email': 'maxipytech@gmail.com',
        'logo': '/static/prebuypc%20logo%20rounded.png',
        'terms': None,
        'owner_name': 'Authorised Signatory'
    }

    # Render HTML to string
    html_string = render_to_string('Invoice/invoice_detail.html', {
        'invoice': invoice,
        'business': business
    })

    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'

    # Generate PDF
    pisa.CreatePDF(html_string, dest=response)

    return response


def invoice_create(request):
    """Create a new invoice"""
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                invoice = form.save()
                # Save only items that have meaningful data
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        service_category = form.cleaned_data.get('service_category')
                        quantity = form.cleaned_data.get('quantity')
                        unit_price = form.cleaned_data.get('unit_price')
                        
                        # Only save if ALL required fields have meaningful values
                        # service_category must not be empty/None and not the default option
                        # quantity must be a number > 0
                        # unit_price must be a number >= 0
                        if (service_category and 
                            str(service_category).strip() not in ['', 'None', '-- Select Category --'] and
                            quantity is not None and quantity > 0 and
                            unit_price is not None and unit_price >= 0):
                            item = form.save(commit=False)
                            item.invoice = invoice
                            item.save()

                # Generate invoice number if not provided
                if not invoice.invoice_number:
                    invoice.invoice_number = f"INV-{invoice.id:04d}"
                    invoice.save()

                messages.success(request, f'Invoice {invoice.invoice_number} created successfully.')
                return redirect('invoices:detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Invoice'
    })


def invoice_edit(request, pk):
    """Edit an existing invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, queryset=invoice.items.all())

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                invoice = form.save()
                # Handle items: save only non-empty, delete if emptied
                for form in formset:
                    if form.cleaned_data:
                        if form.cleaned_data.get('DELETE', False):
                            if form.instance.pk:
                                form.instance.delete()
                        else:
                            if form.cleaned_data.get('DELETE', False):
                                if form.instance.pk:
                                    form.instance.delete()
                            elif (form.cleaned_data.get('service_category') or 
                                  form.cleaned_data.get('quantity') or 
                                  form.cleaned_data.get('unit_price')):
                                item = form.save(commit=False)
                                item.invoice = invoice
                                item.save()
                            elif form.instance.pk:
                                # Existing item now empty, delete it
                                form.instance.delete()
                messages.success(request, f'Invoice {invoice.invoice_number} updated successfully.')
                return redirect('invoices:detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(queryset=invoice.items.all())

    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Edit Invoice',
        'invoice': invoice
    })


def invoice_delete(request, pk):
    """Delete an invoice"""
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f'Invoice {invoice_number} deleted successfully.')
        return redirect('invoices:list')

    return render(request, 'invoices/invoice_confirm_delete.html', {
        'invoice': invoice
    })


def payment_add(request, invoice_pk):
    """Add a payment to an invoice"""
    invoice = get_object_or_404(Invoice, pk=invoice_pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()

            # Update invoice status
            invoice.save()

            messages.success(request, f'Payment of {invoice.currency} {payment.amount} added successfully.')
            return redirect('invoices:detail', pk=invoice.pk)
    else:
        form = PaymentForm()

    return render(request, 'invoices/payment_form.html', {
        'form': form,
        'invoice': invoice
    })


def client_list(request):
    """List all clients"""
    clients = Client.objects.all()
    return render(request, 'invoices/client_list.html', {
        'clients': clients
    })


def client_create(request):
    """Create a new client"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client {client.name} created successfully.')
            return redirect('invoices:client_list')
    else:
        form = ClientForm()

    return render(request, 'invoices/client_form.html', {
        'form': form,
        'title': 'Create Client'
    })


def client_edit(request, pk):
    """Edit a client"""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client {client.name} updated successfully.')
            return redirect('invoices:client_list')
    else:
        form = ClientForm(instance=client)

    return render(request, 'invoices/client_form.html', {
        'form': form,
        'title': 'Edit Client',
        'client': client
    })


def dashboard(request):
    """Dashboard with invoice statistics"""
    total_invoices = Invoice.objects.count()
    total_paid = Invoice.objects.filter(status='paid').count()
    total_overdue = Invoice.objects.filter(status='overdue').count()
    total_clients = Client.objects.count()

    # Calculate total revenue
    total_revenue = sum(invoice.grand_total for invoice in Invoice.objects.filter(status='paid'))

    return render(request, 'invoices/dashboard.html', {
        'total_invoices': total_invoices,
        'total_paid': total_paid,
        'total_overdue': total_overdue,
        'total_clients': total_clients,
        'total_revenue': total_revenue,
    })
