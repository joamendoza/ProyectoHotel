from django import forms
from .models import Hotel, Valoracion, Habitacion, Usuario

class MultipleHabitacionForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), label='Hotel')
    numero_pisos = forms.IntegerField(min_value=1, label='Número de Pisos')
    habitaciones_por_piso = forms.IntegerField(min_value=1, label='Habitaciones por Piso')
    cantidad_camas = forms.IntegerField(min_value=1, label='Cantidad de Camas por Habitación')

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['hotel', 'numero', 'cantidad_camas', 'descripcion', 'ocupada']

class FiltroHabitacionesForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), required=False, label='Hotel')
    ocupada = forms.NullBooleanField(required=False, widget=forms.Select(choices=[
        ('', 'Todas'),
        (True, 'Sí'),
        (False, 'No'),
    ]))
    cantidad_camas = forms.ChoiceField(required=False, label='Cantidad de Camas', choices=[('', 'Todas')])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        camas_choices = [(cantidad, cantidad) for cantidad in Habitacion.objects.values_list('cantidad_camas', flat=True).distinct()]
        self.fields['cantidad_camas'].choices += camas_choices

class FiltroReservasForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), required=False, label='Hotel')
    habitacion = forms.ModelChoiceField(queryset=Habitacion.objects.all(), required=False, label='Habitación')
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), required=False, label='Usuario')
    fecha_salida = forms.DateTimeField(required=False, label='Fecha de Salida', widget=forms.DateInput(attrs={'type': 'date'}))


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ['puntuacion', 'comentario']