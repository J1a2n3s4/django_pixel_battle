from django import forms 

class userform(forms.Form): 
    email = forms.EmailField(max_length = 300)
    name = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)

