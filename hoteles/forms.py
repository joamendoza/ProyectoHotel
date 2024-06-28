from django import forms
from .models import Hotel, Valoracion

class MultipleHabitacionForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), label='Hotel')
    numero_pisos = forms.IntegerField(min_value=1, label='Número de Pisos')
    habitaciones_por_piso = forms.IntegerField(min_value=1, label='Habitaciones por Piso')
    cantidad_camas = forms.IntegerField(min_value=1, label='Cantidad de Camas por Habitación')


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntuacion', 'comentario']