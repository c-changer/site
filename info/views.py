from django.shortcuts import render

# Create your views here.
def partners(request):
    return render(request, "info/partners.html")

def reviews(request):
    return render(request, "info/reviews.html")

def contact(request):
    return render(request, "info/contact.html")

def agreement(request):
    return render(request, "info/agreement.html")

def aml_agreement(request):
    return render(request, "info/aml-agreement.html")
