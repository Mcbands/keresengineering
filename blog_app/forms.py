from django import forms
from .models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact_Us
        fields = ('full_name','email','phone','message')
        labels = {
            'full_name': 'Full Name',
            'email': 'Email',
            'phone': 'phone',
            'message': 'Message',
        }
        widgets={forms.Textarea(attrs={'rows':5, 'cols': 80}), }
       
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['email'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['phone'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['message'].widget.attrs.update({'class': 'form-control'})





