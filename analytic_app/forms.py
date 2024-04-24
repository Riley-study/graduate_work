from django import forms

MONTH_CHOICES = [('1', 'Январь'), ('2', 'Февраль'), ('3', 'Март'), ('4', 'Апрель'), ('5', 'Май'), ('6', 'Июнь'),
                 ('7', 'Июль'), ('8', 'Август'), ('9', 'Сентябрь'), ('10', 'Октябрь'), ('11', 'Ноябрь'),
                 ('12', 'Декабрь'), ]

SHOP_CHOICES = [
    ('1', 'Пекарня_1'), ('2', 'Пекарня_2'), ('3', 'Пекарня_3'), ]

YEAR_CHOICES = [('1', '2023'), # ('2', '2024'),
    ]


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Начало периода (YYYY-MM-DD)')
    end_date = forms.DateField(label='Конец периода (YYYY-MM-DD)')
    shop = forms.ChoiceField(choices=SHOP_CHOICES, label='Выберите пекарню')


class MonthAndYearRangeForm(forms.Form):
    month = forms.ChoiceField(choices=MONTH_CHOICES, label='Выберите месяц')
    year = forms.ChoiceField(choices=YEAR_CHOICES, label='Выберите Год')
    shop = forms.ChoiceField(choices=SHOP_CHOICES, label='Выберите пекарню')


class YearRangeForm(forms.Form):
    year = forms.ChoiceField(choices=YEAR_CHOICES, label='Выберите Год')
    shop = forms.ChoiceField(choices=SHOP_CHOICES, label='Выберите пекарню')