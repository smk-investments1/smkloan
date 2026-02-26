from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

class Customer(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal("0.1175"))
    loan_id = models.CharField(max_length=20, unique=True, editable=False)  # not editable in admin
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-generate Loan ID if not set
        if not self.loan_id:
            today = date.today()
            ddmm = today.strftime("%d%m")
            count_today = Loan.objects.filter(loan_id__startswith=f"SMK{ddmm}").count() + 1
            self.loan_id = f"SMK{ddmm}L{count_today:03d}"

        # Correct monthly installment formula:
        # (principal / duration) + (principal * interest_rate)
        principal = self.principal
        months = self.duration
        rate = self.interest_rate

        installment = (principal / Decimal(months)) + (principal * rate)
        self.monthly_installment = installment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Salary safeguard
        if self.monthly_installment > (self.customer.salary / Decimal("2")):
            raise ValueError("Monthly installment exceeds 50% of salary")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.loan_id} - {self.customer.name}"


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    proof = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Pending", "Pending")])

    def __str__(self):
        return f"{self.loan.loan_id} - {self.amount} on {self.date}"


class Reminder(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    reminder_date = models.DateField()
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[("Sent", "Sent"), ("Pending", "Pending")])

    def __str__(self):
        return f"Reminder for {self.loan.loan_id} on {self.reminder_date}"
