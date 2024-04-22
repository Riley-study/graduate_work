
from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Начало периода (YYYY-MM-DD)')
    end_date = forms.DateField(label='Конец периода (YYYY-MM-DD)')


class MonthAndYearRangeForm(forms.Form):
    MONTH_CHOICES = [
        ('1', 'Январь'),
        ('2', 'Февраль'),
        ('3', 'Март'),
        ('4', 'Апрель'),
        ('5', 'Май'),
        ('6', 'Июнь'),
        ('7', 'Июль'),
        ('8', 'Август'),
        ('9', 'Сентябрь'),
        ('10', 'Октябрь'),
        ('11', 'Ноябрь'),
        ('12', 'Декабрь'),
    ]
    month = forms.ChoiceField(choices=MONTH_CHOICES, label='Выберите месяц')
    YEAR_CHOICES = [
        ('1', '2023'),
        # ('2', '2024'),
    ]
    year = forms.ChoiceField(choices=YEAR_CHOICES, label='Выберите Год')
