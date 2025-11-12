from django import forms
from django.forms import inlineformset_factory
from .models import Deck, DeckCard, Card

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']

# Formset to handle card quantities
DeckCardFormSet = inlineformset_factory(
    Deck,
    DeckCard,
    fields=('card', 'quantity'),
    extra=0,
    can_delete=True,
    widgets={
        'quantity': forms.NumberInput(attrs={'style':'width:50px'})
    }
)
