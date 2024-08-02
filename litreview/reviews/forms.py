from django import forms
from .models import Ticket, Review
from django.contrib.auth.models import User


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]


class UserFollowForm(forms.Form):
    username = forms.CharField(max_length=150)
