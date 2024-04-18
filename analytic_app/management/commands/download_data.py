from django.core.management.base import BaseCommand
from analytic_app.models import Revenue_daily, Costs_by_month, Product
import pandas as pd


def read_excel_data(file_path):
    df = pd.read_excel(file_path)
    return df


class Command(BaseCommand):
    help = "Download data from .xlsx"

    # def handle(self, *args, **kwargs):
    #     excel_data = read_excel_data("data/list_of_product.xlsx")
    #     for index, row in excel_data.iterrows():
    #         product = Product(product_name=row['product_name'])
    #         product.save()

    # def handle(self, *args, **kwargs):
    #     excel_data = read_excel_data("data/Costs_2023.xlsx")
    #     for index, row in excel_data.iterrows():
    #         cost = Costs_by_month(cost_name_id=row['cost_id'],
    #                                  date=row['date'],
    #                                  month=row['month'],
    #                                  bakery_address_id=row['bakery_address_id'],
    #                                  amount_of_costs=row['amount_of_costs'],)
    #         cost.save()

    def handle(self, *args, **kwargs):
        excel_data = read_excel_data("data/Sales_01.01.23_31.03.23.xlsx")
        list_of_revenue = []
        for index, row in excel_data.iterrows():
            revenue = Revenue_daily(product_name_id=row['product_name_id'],
                                    date=row['date'],
                                    month=row['month'],
                                    bakery_address_id=row['bakery_address_id'],
                                    quantity=row['quantity'],
                                    price=row['price'],
                                    total_sum=row['total_sum'], )
            list_of_revenue.append(revenue)
        Revenue_daily.objects.bulk_create(list_of_revenue)
