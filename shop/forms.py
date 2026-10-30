from django import forms

from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email address", "aria-label": "Email address"})
        }
