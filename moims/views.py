from django.shortcuts import render

# Create your views here.
def many(request):
    return render(request, 'moims/many.html')