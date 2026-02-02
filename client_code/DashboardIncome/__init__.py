from ._anvil_designer import DashboardIncomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import datetime

class DashboardIncome(DashboardIncomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_income_dashboard_data()
    
  def load_income_dashboard_data(self):
    dashboard_data = anvil.server.call('get_income_dashboard_data')
    self.rendas_mes.text = f"R$ {dashboard_data['total_income']:.2f}"

    self.grafico_rendas.data = [
      go.Bar(
        x=list(dashboard_data['income_by_month'].keys()),
        y=list(dashboard_data['income_by_month'].values()),
        name="Income"
      )
    ]

@anvil.server.callable
def get_income_dashboard_data():
  today = datetime.date.today()
  current_month = today.strftime("%B")
  current_year = today.year

  total_income = sum([i['value'] for i in app_tables.income.search(month=current_month, year=current_year)])

  income_by_month = {}
  for i in app_tables.income.search():
    month_year = i['date'].strftime("%Y-%m")
    if month_year not in income_by_month:
      income_by_month[month_year] = 0
    income_by_month[month_year] += i['value']

  return {
    'total_income': total_income,
    'income_by_month': income_by_month
  }