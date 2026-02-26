from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Loan, Payment, Reminder

# Home page view
def home(request):
    return render(request, "loans/home.html")

# Login page view
def login_page(request):
    error = None
    if request.method == "POST":
        loan_id = request.POST.get("loan_id")
        phone = request.POST.get("phone")

        try:
            loan = Loan.objects.get(loan_id=loan_id, customer__phone=phone)
            payments = Payment.objects.filter(loan=loan)
            reminders = Reminder.objects.filter(loan=loan)
            return render(request, "loan_dashboard.html", {
                "loan": loan,
                "payments": payments,
                "reminders": reminders
            })
        except Loan.DoesNotExist:
            error = "Invalid Loan ID or Phone Number"

    return render(request, "login.html", {"error": error})

# Logout view
def logout_view(request):
    logout(request)
    return redirect("/login/")
