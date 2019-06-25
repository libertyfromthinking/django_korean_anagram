from django import forms

class AnagramForm(forms.Form):
    search_word = forms.CharField(label='',widget=forms.TextInput(attrs={'id':"search_input", 'placeholder':"Search..."}))
    