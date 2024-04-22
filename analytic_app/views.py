from django.shortcuts import render
# from django.http import HttpResponse
import pandas as pd
import os
import matplotlib.pyplot as plt
from .models import Revenue_daily, Costs_by_month
from django.conf import settings
# from io import BytesIO
# import base64
# from django.http import JsonResponse
from django.db.models import Sum
from .forms import DateRangeForm

MONTH_DICT = {
    "01": "январь",
    "02": "февраль",
    "03": "март",
    "04": "апрель",
    "05": "май",
    "06": "июнь",
    "07": "июль",
    "08": "август",
    "09": "сентябрь",
    "10": "октябрь",
    "11": "ноябрь",
    "12": "декабрь"
}

def generate_histogram(start_date, end_date):
    revenue_data = Revenue_daily.objects.filter(date__range=[start_date, end_date]).values(
        'product_name_id__product_name').annotate(total_sum=Sum('total_sum')).order_by('-total_sum')[:10]
    product_names = [item['product_name_id__product_name'] for item in revenue_data]
    total_revenues = [item['total_sum'] for item in revenue_data]
    plt.bar(product_names, total_revenues)
    plt.xlabel('Наименование')
    plt.ylabel('Выручка')
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
    total_expenses = Costs_by_month.objects.filter(month=selected_month).aggregate(total=Sum('amount_of_costs'))['total']
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


def index(request):
    return render(request, 'analytic_app/main_page.html')


def sales(request):
    if request.method == 'POST':
        selected_month = request.POST.get('selected_month')
        selected_year = request.POST.get('selected_year')
        selected_month_name = MONTH_DICT[selected_month]
        image_url = generate_graph(selected_month)
        return render(request, 'analytic_app/sales.html',
                      {'chart_image': image_url, 'selected_month': selected_month_name, 'selected_year': selected_year})
    else:
        return render(request, 'analytic_app/select_month_and_year.html')


def costs(request):
    if request.method == 'POST':
        selected_month = request.POST.get('selected_month')
        selected_year = request.POST.get('selected_year')
        selected_month_name = MONTH_DICT[selected_month]
        image_url = generate_diagram(selected_month)
        return render(request, 'analytic_app/costs.html',
                      {'chart_image': image_url, 'selected_month': selected_month_name, 'selected_year': selected_year})
    else:
        return render(request, 'analytic_app/select_month_and_year.html')


def product_range_by_revenue(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            image_url = generate_histogram(start_date, end_date)
            return render(request, 'analytic_app/product_range.html',
                          {'chart_image': image_url, 'start_date': start_date, 'end_date': end_date})
    else:
        form = DateRangeForm()
    return render(request, 'analytic_app/product_range.html',
                  {'form': form})


def profitability(request):
    return render(request, 'analytic_app/profitability.html')


def forecasts(request):
    return render(request, 'analytic_app/forecasts.html')


def indicators_by_point_of_sale(request):
    image_url = '/media/sales_chart.png'  # Путь к вашему изображению в папке media
    return render(request, 'analytic_app/indicators_by_point_of_sale.html', {'image_url': image_url})

# def my_view_1(request):
#     image_url = '/media/sales_chart.png'  # Путь к вашему изображению в папке media
#     return render(request, 'test.html')
