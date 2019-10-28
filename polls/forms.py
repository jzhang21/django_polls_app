from django import forms
from .models import Suggestion

class SuggestionForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    text = forms.CharField( max_length=500, widget=forms.Textarea)
    class Meta:
        model = Suggestion
        fields = ('name', 'text')
