from django.core.management.base import BaseCommand
from django.utils import timezone
from invoices.models import Client, Invoice, InvoiceItem, Payment
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate sample data for testing'

    def handle(self, *args, **options):
        # Check if data already exists
        if Invoice.objects.exists():
            self.stdout.write(self.style.WARNING('Sample data already exists. Skipping population.'))
            return

        # Create sample clients
        client1 = Client.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='+254712345678',
            company_name='Doe Enterprises Ltd',
            billing_address='123 Main St, Nairobi, Kenya',
            kra_pin='A123456789B'
        )

        client2 = Client.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            phone='+254798765432',
            company_name='Smith Consulting',
            billing_address='456 Business Ave, Nairobi, Kenya',
            kra_pin='B987654321C'
        )

        self.stdout.write(self.style.SUCCESS('Created sample clients'))

        # Create sample invoices (without saving totals yet)
        invoice1 = Invoice(
            invoice_number='INV-0001',
            client=client1,
            currency='KES',
            date_issued=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=30),
            status='sent',
            tax_rate=16,
            discount=0,
            notes='Thank you for your business!'
        )
        invoice1.save()  # Save without calculating totals

        invoice2 = Invoice(
            invoice_number='INV-0002',
            client=client2,
            currency='KES',
            date_issued=timezone.now().date() - timedelta(days=15),
            due_date=timezone.now().date() - timedelta(days=5),
            status='paid',
            tax_rate=16,
            discount=5000,
            notes='PC hardware consultation and setup'
        )
        invoice2.save()  # Save without calculating totals

        self.stdout.write(self.style.SUCCESS('Created sample invoices'))

        # Create invoice items
        InvoiceItem.objects.create(
            invoice=invoice1,
            service_category='PC Hardware Consultation',
            detail_notes='Initial consultation for gaming PC build',
            quantity=2,
            unit_price=15000
        )

        InvoiceItem.objects.create(
            invoice=invoice1,
            service_category='Component Sourcing',
            detail_notes='Research and sourcing of PC components',
            quantity=1,
            unit_price=25000
        )

        InvoiceItem.objects.create(
            invoice=invoice2,
            service_category='Complete PC Build',
            detail_notes='Custom gaming PC assembly and testing',
            quantity=1,
            unit_price=120000
        )

        InvoiceItem.objects.create(
            invoice=invoice2,
            service_category='Software Installation',
            detail_notes='Windows installation and driver setup',
            quantity=1,
            unit_price=10000
        )

        self.stdout.write(self.style.SUCCESS('Created sample invoice items'))

        # Create payments
        Payment.objects.create(
            invoice=invoice2,
            amount=135000,
            method='mpesa',
            reference='RF123456789',
            phone='+254712345678'
        )

        self.stdout.write(self.style.SUCCESS('Created sample payments'))

        # Update invoice totals
        invoice1.save()  # This will calculate totals now that items exist
        invoice2.save()  # This will calculate totals now that items exist

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
        self.stdout.write('You can now visit http://127.0.0.1:8000/ to see the system in action.')