from django.http import JsonResponse
from django.shortcuts import render
from hoteles.models import Hotel

# Create your views here.
def get_hoteles(request):
    hoteles = list(Hotel.objects.values())
    return JsonResponse(hoteles, safe=False)

def hoteles_api(request):
    categoria = request.GET.get('categoria')
    en_oferta = request.GET.get('en_oferta')

    if categoria:
        hoteles = Hotel.objects.filter(categoria=categoria)
    elif en_oferta:
        hoteles = Hotel.objects.filter(en_oferta=True)
    else:
        hoteles = Hotel.objects.all()

    data = [{
        'id': hotel.id,
        'nombre': hotel.nombre,
        'descripcion_breve': hotel.descripcion_breve,
        'descripcion_detallada': hotel.descripcion_detallada,
        'precio': hotel.precio,
        'precio_con_descuento': hotel.precio_con_descuento(),
        'foto': hotel.foto.url,
        'en_oferta': hotel.en_oferta,
        'porcentaje_descuento': hotel.porcentaje_descuento,
        'categoria': hotel.categoria,
    } for hotel in hoteles]

    return JsonResponse(data, safe=False)