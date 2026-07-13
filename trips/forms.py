from django import forms
from .models import Trip


class TripPlannerStep1Form(forms.Form):
    destination = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Kyoto, Japan',
            'class': 'w-full pl-12 pr-4 py-4 rounded-xl border border-outline-variant focus:ring-2 focus:ring-secondary focus:border-secondary transition-all bg-surface',
        })
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full pl-12 pr-4 py-4 rounded-xl border border-outline-variant focus:ring-2 focus:ring-secondary focus:border-secondary transition-all bg-surface',
        }),
        required=False,
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full pl-12 pr-4 py-4 rounded-xl border border-outline-variant focus:ring-2 focus:ring-secondary focus:border-secondary transition-all bg-surface',
        }),
        required=False,
    )
    traveler_count = forms.IntegerField(
        min_value=1, max_value=50, initial=2,
        widget=forms.HiddenInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', 'End date must be on or after start date.')
        return cleaned_data


class TripPlannerStep2Form(forms.Form):
    BUDGET_CHOICES = [
        ('budget', 'Budget'),
        ('mid', 'Mid-range'),
        ('luxury', 'Luxury'),
    ]
    STYLE_CHOICES = [
        ('Adventure', 'Adventure'),
        ('Family', 'Family'),
        ('Solo', 'Solo'),
        ('Cultural', 'Cultural'),
        ('Relaxing', 'Relaxing'),
        ('Foodie', 'Foodie'),
        ('Romantic', 'Romantic'),
        ('Wildlife', 'Wildlife'),
    ]

    budget = forms.ChoiceField(
        choices=BUDGET_CHOICES,
        widget=forms.RadioSelect,
        initial='mid',
    )
    travel_styles = forms.MultipleChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class TripSaveForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'destination_name', 'start_date', 'end_date',
                  'traveler_count', 'budget', 'travel_styles']
