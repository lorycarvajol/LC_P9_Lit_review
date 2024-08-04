from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

    title = forms.CharField(max_length=128, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    image = forms.ImageField(required=False)
