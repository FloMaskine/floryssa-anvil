from ._anvil_designer import GraficosTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime


class Graficos(GraficosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.graficos_datepicker.date = datetime.date.today()
    self.load_plots()

  def load_plots(self, **event_args):
    month = self.graficos_datepicker.date.strftime("%B")
    year = self.graficos_datepicker.date.year
    self.label_mes_selecionado.text = f"{month} {year}"

    expenses = anvil.server.call('get_expenses_by_month', month, year)
    income = anvil.server.call('get_income_by_month', month, year)
    expenses_by_category = anvil.server.call('get_expenses_by_category', month, year)

    # Plot 1: Income vs Expenses Bar Chart
    expense_values = [e['value'] for e in expenses]
    income_values = [i['value'] for i in income]

    fig1 = go.Figure(data=[
      go.Bar(name='Income', x=['Total'], y=[sum(income_values)]),
      go.Bar(name='Expenses', x=['Total'], y=[sum(expense_values)])
    ])
    fig1.update_layout(barmode='group', title_text='Income vs Expenses')
    self.plot_1.figure = fig1

    # Plot 2: Expenses by Category Pie Chart (using the plot_2 component)
    if hasattr(self, 'plot_2'): # Check if plot_2 exists
      labels = list(expenses_by_category.keys())
      values = list(expenses_by_category.values())
      fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
      fig2.update_layout(title_text='Expenses by Category')
      self.plot_2.figure = fig2


  def graficos_datepicker_change(self, **event_args):
    """This method is called when the date is changed"""
    self.load_plots()
