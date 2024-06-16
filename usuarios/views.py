from django.http import JsonResponse
from django.shortcuts import render
from hoteles.models import Hotel

# Create your views here.
def get_hoteles(request):
    hoteles = list(Hotel.objects.values())
    return JsonResponse(hoteles, safe=False)