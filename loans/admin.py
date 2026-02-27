from django.contrib import admin
from .models import Customer, Loan, Payment, Reminder

admin.site.register(Customer)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(Reminder)
