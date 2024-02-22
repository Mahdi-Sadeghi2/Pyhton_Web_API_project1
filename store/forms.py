from django import forms 
from .models import UserComment

class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='Quantity')
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ['comment_text']