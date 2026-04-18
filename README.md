# PreBuyPc Invoice System

A comprehensive Django-based invoicing system for PreBuyPc consultancy services.

## Features

- **Client Management**: Create and manage client information
- **Invoice Creation**: Generate professional invoices with line items
- **Payment Tracking**: Record payments manually (M-Pesa, cash, bank transfer)
- **Status Management**: Track invoice status (draft, sent, paid, overdue, etc.)
- **Public Sharing**: Share invoices via secure public links
- **Tax & Discount Support**: Apply taxes and discounts to invoices
- **Responsive Design**: Mobile-friendly invoice display

## Installation & Setup

1. **Clone or set up the project**
2. **Install dependencies** (Django is already included)
3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Populate sample data** (optional):
   ```bash
   python manage.py populate_sample_data
   ```
5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
6. **Access the application** at `http://127.0.0.1:8000/`

## Usage

### Dashboard
- View system statistics
- Quick access to create invoices and clients

### Clients
- **List Clients**: View all clients
- **Add Client**: Create new client with contact information
- **Edit Client**: Update client details

### Invoices
- **List Invoices**: View all invoices with status indicators
- **Create Invoice**:
  - Select or create a client
  - Add multiple line items with quantities and prices
  - Set tax rate and discounts
  - System automatically calculates totals
- **Edit Invoice**: Modify invoice details and items
- **View Invoice**: See detailed invoice information
- **Public View**: Share invoice via UUID-based public link
- **Add Payment**: Record payments against invoices

### Admin Interface
Access Django admin at `/admin/` for full data management.

## Models

### Client
- Name, email, phone, company
- Billing address, KRA PIN
- Notes and timestamps

### Invoice
- Unique invoice number
- Client relationship
- Currency, dates, status
- Tax rate, discount, calculated totals
- Public sharing token

### InvoiceItem
- Service category and details
- Quantity, unit price, calculated total

### Payment
- Amount, method (M-Pesa/Cash/Bank)
- Reference numbers, phone numbers
- Timestamps

## Status Logic

- **Draft**: Initial state
- **Sent**: Invoice sent to client
- **Paid**: All amounts paid
- **Overdue**: Past due date and unpaid
- **Cancelled/Refunded**: Special states

## Security Features

- CSRF protection
- Input validation
- UUID-based public links
- No authentication required for public invoice viewing

## Future Enhancements

- User authentication and permissions
- PDF export functionality
- Email notifications
- Multi-currency support
- Reporting dashboard
- API endpoints

## Technical Details

- **Framework**: Django 6.0.3
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, Custom CSS
- **Architecture**: MTV pattern with class-based views

## Development

The system follows Django best practices:
- Model relationships with proper constraints
- Form validation and error handling
- Template inheritance
- Admin integration
- Management commands for data setup

## License

This project is developed for PreBuyPc consultancy services.