from django import forms

class ContactForm(forms.Form):
    region = forms.CharField(max_length=100, label='region')