from django.contrib import admin
from django.urls import path, include
from .views import index, sales, costs, product_range_by_revenue, profitability, import_file

urlpatterns = [
    path('', index, name='index'),
    path('sales/', sales, name='sales'),
    path('costs/', costs, name='costs'),
    # path('selected_month/', costs, name='selected_month'),
    path('product_range/', product_range_by_revenue, name='product_range'),
    path('profitability/', profitability, name='profitability'),
    path('import/', import_file, name='import_file'),

]
