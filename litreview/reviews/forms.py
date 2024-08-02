from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
