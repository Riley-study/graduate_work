from django.contrib import admin
from django.urls import path, include
from .views import index, sales, costs, product_range_by_revenue, profitability, forecasts, indicators_by_point_of_sale

urlpatterns = [
    path('', index, name='index'),
    path('sales/', sales, name='sales'),
    path('costs/', costs, name='costs'),
    path('selected_month/', costs, name='selected_month'),
    path('product_range/', product_range_by_revenue, name='product_range'),
    path('profitability/', profitability, name='profitability'),
    path('forecasts/', forecasts, name='forecasts'),
    path('indicators_by_point_of_sale/', indicators_by_point_of_sale, name='indicators_by_point_of_sale'),

]
