
from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Начало периода (YYYY-MM-DD)')
    end_date = forms.DateField(label='Конец периода (YYYY-MM-DD)')