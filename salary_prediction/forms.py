from django import forms

class SalaryForm(forms.Form):
    experience = forms.FloatField(
        label= 'Years of Experience')