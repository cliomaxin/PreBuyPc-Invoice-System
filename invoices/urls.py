from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Invoices
    path('invoices/', views.invoice_list, name='list'),
    path('invoices/create/', views.invoice_create, name='create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='detail'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='edit'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='delete'),
    path('invoices/<int:invoice_pk>/payment/', views.payment_add, name='add_payment'),

    # Public invoice view
    path('invoice/<uuid:token>/', views.invoice_public, name='public'),
    path('invoice/<uuid:token>/pdf/', views.invoice_pdf, name='pdf'),

    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
]