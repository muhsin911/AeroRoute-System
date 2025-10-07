from django import forms
from .models import AirportRoute, Airport


class AirportRouteForm(forms.ModelForm):
    """
    Form to create or edit an AirportRoute instance.

    The front-end allows the user to select 'from' and 'to' airports,
    specify the route position (left or right), and enter the route duration.
    """
    class Meta:
        # Associates this form directly with the AirportRoute model
        model = AirportRoute

        # Fields to include in the form, corresponding to model fields
        fields = ['from_airport', 'to_airport', 'position', 'duration']

    def clean(self):
        """
        Custom form validation logic to avoid creating routes with same
        origin and destination airports.

        Raises:
            forms.ValidationError: If from_airport and to_airport are the same.
        """
        cleaned = super().clean()
        if cleaned.get('from_airport') and cleaned.get('to_airport'):
            if cleaned['from_airport'] == cleaned['to_airport']:
                raise forms.ValidationError("From and To airports must be different.")
        return cleaned


class NthNodeSearchForm(forms.Form):
    """
    Form for searching the Nth left or right node from a starting airport.

    Fields:
        - airport_code: the code of the airport to start traversal from
        - direction: 'left' or 'right' direction for traversal
        - n: the Nth node index to find (1 means immediate child)
    """
    airport_code = forms.CharField(max_length=10, label="Start Airport Code")
    direction = forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right')])
    n = forms.IntegerField(min_value=1, label="N (1 = immediate child)")


class ShortestNodeSearchForm(forms.Form):
    """
    Form for searching the shortest path between two airports.

    Fields:
        - from_airport: starting airport code
        - to_airport: destination airport code
    """
    from_airport = forms.CharField(max_length=10)
    to_airport = forms.CharField(max_length=10)
