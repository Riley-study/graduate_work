from django.shortcuts import render
import logging
import pandas as pd
import os
import matplotlib.pyplot as plt
from .models import Revenue_daily, Costs_by_month
from django.conf import settings
from django.db.models import Sum
from .forms import DateRangeForm, MonthAndYearRangeForm, YearRangeForm
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import F, Func
from datetime import datetime
from calendar import month_name

logger = logging.getLogger(__name__)
MONTH_DICT = {
    "1": "январь",
    "2": "февраль",
    "3": "март",
    "4": "апрель",
    "5": "май",
    "6": "июнь",
    "7": "июль",
    "8": "август",
    "9": "сентябрь",
    "10": "октябрь",
    "11": "ноябрь",
    "12": "декабрь"
}
YEAR_DICT = {
    "1": "2023",
    "2": "2024",
}


def generate_histogram(start_date, end_date):
    revenue_data = Revenue_daily.objects.filter(date__range=[start_date, end_date]).values(
        'product_name_id__product_name').annotate(total_sum=Sum('total_sum')).order_by('-total_sum')[:10]
    product_names = [item['product_name_id__product_name'] for item in revenue_data]
    total_revenues = [item['total_sum'] for item in revenue_data]
    plt.bar(product_names, total_revenues)
    # for i in range(len(product_names)):
    #     plt.text(i, total_revenues[i], str(total_revenues[i]), ha='center', va='bottom')
    # plt.xlabel('Наименование')
    plt.ylabel('Выручка, руб.')
    plt.xticks(rotation=75)
    plt.tight_layout()
    plt.savefig('media/product_range.png')
    image_url = '/media/product_range.png'
    return image_url


def generate_graph(selected_month):
    sales_data = Revenue_daily.objects.filter(month=selected_month)
    df = pd.DataFrame(list(sales_data.values('date', 'total_sum')))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['total_sum'], marker='o', linestyle='-')
    plt.xlabel('Дата')
    plt.ylabel('Сумма продаж, руб.')
    plt.xticks(rotation=45)
    plt.grid(False)
    plt.tight_layout()
    plt.savefig('media/sales_chart_2.png')
    image_url = '/media/sales_chart_2.png'
    return image_url


def generate_diagram(selected_month):
    expenses = Costs_by_month.objects.filter(month=selected_month).select_related('cost_name_id').values(
        'cost_name_id__cost_name').annotate(total_expenses=Sum('amount_of_costs'))
    total_expenses = Costs_by_month.objects.filter(month=selected_month).aggregate(total=Sum('amount_of_costs'))[
        'total']
    categories = [expense['cost_name_id__cost_name'] for expense in expenses]
    expenses_amounts = [expense['total_expenses'] for expense in expenses]
    labels = [f"{category} " for category, expense_amount in zip(categories, expenses_amounts)]
    plt.figure(figsize=(8, 8))
    colors = ['#1f77b4', '#aec7e8', '#6baed6', '#98abc5', '#c6dbef']
    plt.pie(expenses_amounts, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
            explode=[0.2] * len(expenses_amounts), shadow=True)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('media/costs.png')
    image_url = '/media/costs.png'
    return image_url


def generate_profit_graph(selected_year):
    revenue_data = Revenue_daily.objects.filter(date__year=selected_year)

    # Получаем данные о продажах за каждый месяц
    monthly_sales = Revenue_daily.objects.values('month').annotate(total_sales=Sum('total_sum'))
    monthly_costs = Costs_by_month.objects.values('month').annotate(total_costs=Sum('amount_of_costs'))

    # Создаем списки для хранения месяцев и сумм продаж
    months = []
    sales = []
    costs = []

    # Проходимся по результатам агрегации и добавляем данные в списки
    for item in monthly_sales:
        # Преобразуем номер месяца в название месяца
        name_of_month = month_name[item['month']]
        months.append(name_of_month)
        sales.append(item['total_sales'])

    for item in monthly_costs:
        costs.append(item['total_costs'])

    profitability = [((x - y) / x * 100) for x, y in zip(sales, costs)]

    # Строим график
    plt.figure(figsize=(10, 6))
    plt.bar(months, profitability, color='skyblue')
    # plt.plot(months, costs, marker='s', linestyle='-', label='Costs')
    plt.xlabel('Месяц')
    plt.ylabel('Значение в %')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('media/profit.png')
    image_url = '/media/profit.png'
    return image_url


def index(request):
    logger.info('Home page accessed')
    image_url = '/media/logo.png'
    return render(request, 'analytic_app/main_page.html',  {'chart_image': image_url})


def sales(request):
    if request.method == 'POST':
        logger.debug('Page with sales accessed')
        form = MonthAndYearRangeForm(request.POST)
        if form.is_valid():
            selected_month = form.cleaned_data['month']
            selected_year = form.cleaned_data['year']
            selected_month_name = MONTH_DICT[selected_month]
            selected_year_name = YEAR_DICT[selected_year]
            image_url = generate_graph(selected_month)
        return render(request, 'analytic_app/sales.html',
                      {'chart_image': image_url, 'selected_month': selected_month_name,
                       'selected_year': selected_year_name})
    else:
        logger.debug('Page with empty form accessed')
        form = MonthAndYearRangeForm()
        return render(request, 'analytic_app/sales.html', {'form': form})


def costs(request):
    if request.method == 'POST':
        logger.debug('Page with costs accessed')
        form = MonthAndYearRangeForm(request.POST)
        if form.is_valid():
            selected_month = form.cleaned_data['month']
            selected_year = form.cleaned_data['year']
            selected_month_name = MONTH_DICT[selected_month]
            selected_year_name = YEAR_DICT[selected_year]
            image_url = generate_diagram(selected_month)
            return render(request, 'analytic_app/costs.html',
                          {'chart_image': image_url, 'selected_month': selected_month_name,
                           'selected_year': selected_year})
    else:
        logger.debug('Page with empty form accessed')
        form = MonthAndYearRangeForm()
        return render(request, 'analytic_app/costs.html', {'form': form})


def product_range_by_revenue(request):
    if request.method == 'POST':
        logger.debug('Page with range of product accessed')
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            image_url = generate_histogram(start_date, end_date)
            return render(request, 'analytic_app/product_range.html',
                          {'chart_image': image_url, 'start_date': start_date, 'end_date': end_date})
    else:
        logger.debug('Page with empty form accessed')
        form = DateRangeForm()
    return render(request, 'analytic_app/product_range.html',
                  {'form': form})


def import_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        with open('media/' + uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return render(request, 'analytic_app/import.html', {'filename': uploaded_file.name})
    return render(request, 'analytic_app/import.html')

def profitability(request):
    if request.method == 'POST':
        logger.debug('Page with sales accessed')
        form = YearRangeForm(request.POST)
        if form.is_valid():
            selected_year = form.cleaned_data['year']
            selected_year_name = YEAR_DICT[selected_year]
            image_url = generate_profit_graph(selected_year)
        return render(request, 'analytic_app/profitability.html',
                      {'chart_image': image_url, 'selected_year': selected_year_name})
    else:
        logger.debug('Page with empty form accessed')
        form = YearRangeForm()
        return render(request, 'analytic_app/profitability.html', {'form': form})
