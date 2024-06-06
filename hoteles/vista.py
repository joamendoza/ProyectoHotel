from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
def infoHoteles(request):
    return render(request, 'infoHoteles.html')