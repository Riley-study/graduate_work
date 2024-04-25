from django.test import TestCase
import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from .views import generate_graph, generate_diagram, generate_profit_graph


class TestTemplates(TestCase):
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


    def test_sales(self):
        response = self.client.get('/sales/')
        self.assertEqual(response.status_code, 200)


    def test_costs(self):
        response = self.client.get('/costs/')
        self.assertEqual(response.status_code, 200)


    def test_product_range(self):
        response = self.client.get('/product_range/')
        self.assertEqual(response.status_code, 200)


    def test_profitability(self):
        response = self.client.get('/profitability/')
        self.assertEqual(response.status_code, 200)


    def test_import(self):
        response = self.client.get('/import/')
        self.assertEqual(response.status_code, 200)


class TestGenerateGraph(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch('analytic_app.views.Revenue_daily.objects.filter')
    def test_generate_graph(self, mock_filter):
        mock_sales_data = MagicMock()
        mock_filter.return_value = mock_sales_data
        mock_sales_data.values.return_value = [{'date': '2023-01-01', 'total_sum': 100},
                                               {'date': '2023-01-02', 'total_sum': 200}]

        request = self.factory.post('/', {'month': '1'})
        image_url = generate_graph(request)

        self.assertEqual(image_url, '/media/sales_chart_2.png')


class TestGenerateDiagram(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('analytic_app.views.Costs_by_month.objects.filter')
    def test_generate_diagram(self, mock_filter):
        mock_expenses = MagicMock()
        mock_filter.return_value = mock_expenses
        mock_expenses.select_related.return_value.values.return_value = [
            {'cost_name_id__cost_name': 'Rent', 'total_expenses': 500},
            {'cost_name_id__cost_name': 'Salary', 'total_expenses': 800}]

        request = self.factory.post('/', {'month': '1'})
        image_url = generate_diagram(request)

        self.assertEqual(image_url, '/media/costs.png')


class TestGenerateProfitGraph(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('analytic_app.views.Revenue_daily.objects.filter')
    @patch('analytic_app.views.Costs_by_month.objects.values')
    def test_generate_profit_graph(self, mock_filter_costs, mock_filter_revenue):
        mock_sales_data = MagicMock()
        mock_filter_revenue.return_value = mock_sales_data
        mock_sales_data.values.return_value = [{'month': 1, 'total_sales': 1000}, {'month': 2, 'total_sales': 1500}]

        mock_costs_data = MagicMock()
        mock_filter_costs.return_value = mock_costs_data
        mock_costs_data.return_value = [{'month': 1, 'total_costs': 500}, {'month': 2, 'total_costs': 600}]

        request = self.factory.post('/', {'year': '1'})
        image_url = generate_profit_graph(request)

        self.assertEqual(image_url, '/media/profit.png')


if __name__ == '__main__':
    unittest.main()

