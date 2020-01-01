from django import forms
class usernameform(forms.Form):
	username = forms.CharField()
class textinputform(forms.Form):
	feedback = forms.CharField(widget = forms.Textarea())