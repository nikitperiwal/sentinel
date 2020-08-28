from django import forms


class ScrapeForm(forms.Form):
    keywords = forms.CharField(label='Keywords: ')
    exclude = forms.CharField(label='Exclude words: ')
    #since = forms.DateWidget(label="Since date: ")
    #until = forms.DateWidget(label="To date: ")
