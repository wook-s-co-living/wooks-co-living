from django.shortcuts import render

# Create your views here.

def market_index_view(request):
    
    return render(request, 'markets/index.html')