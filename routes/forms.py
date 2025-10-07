# routes/forms.py
from django import forms
from .models import AirportRoute, Airport

class AirportRouteForm(forms.ModelForm):
    """
    Form to create a route. The front-end will let user select airports by code/name.
    """
    class Meta:
        model = AirportRoute
        fields = ['from_airport', 'to_airport', 'position', 'duration']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('from_airport') and cleaned.get('to_airport'):
            if cleaned['from_airport'] == cleaned['to_airport']:
                raise forms.ValidationError("From and To airports must be different.")
        return cleaned

class NthNodeSearchForm(forms.Form):
    airport_code = forms.CharField(max_length=10, label="Start Airport Code")
    direction = forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right')])
    n = forms.IntegerField(min_value=1, label="N (1 = immediate child)")

class ShortestNodeSearchForm(forms.Form):
    from_airport = forms.CharField(max_length=10)
    to_airport = forms.CharField(max_length=10)
