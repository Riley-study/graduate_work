from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Revenue_daily


def index(request):
    return render(request, 'analytic_app/main_page.html')


def sales(request):
    return render(request, 'analytic_app/sales.html')


def costs(request):
    return render(request, 'analytic_app/costs.html')


def product_range(request):
    return render(request, 'analytic_app/product_range.html')


def profitability(request):
    return render(request, 'analytic_app/profitability.html')


def forecasts(request):
    return render(request, 'analytic_app/forecasts.html')


def indicators_by_point_of_sale(request):
    return render(request, 'analytic_app/indicators_by_point_of_sale.html')

