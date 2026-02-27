from django.db import models

# Customer model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


# Loan model
class Loan(models.Model):
    loan_id = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ("Active", "Active"),
        ("Closed", "Closed"),
        ("Defaulted", "Defaulted"),
    ], default="Active")

    def __str__(self):
        return f"Loan {self.loan_id} - {self.customer.name}"


# Payment model
class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.loan.loan_id} - {self.amount} on {self.date}"


# Reminder model
class Reminder(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    date = models.DateField()
    message = models.TextField()

    def __str__(self):
        return f"Reminder for {self.loan.loan_id} on {self.date}"
