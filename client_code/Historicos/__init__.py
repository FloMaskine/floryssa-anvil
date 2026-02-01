from ._anvil_designer import HistoricosTemplate
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

class Historicos(HistoricosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    today = datetime.date.today()
    self.historico_gastos_datepicker.date = today.replace(day=1)
    self.historico_receitas_datepicker_copy.date = today
    self.load_expenses()
    self.load_income()

  def load_expenses(self, **event_args):
    start_date = self.historico_gastos_datepicker.date
    end_date = datetime.date.today() # or some other end date
    expenses = anvil.server.call('get_expenses_by_date', start_date, end_date)
    self.historico_gastos_list.items = expenses
    self.plot_1.data = self.create_expense_plot(expenses)

  def load_income(self, **event_args):
    start_date = self.historico_receitas_datepicker_copy.date
    end_date = datetime.date.today() # or some other end date
    income = anvil.server.call('get_income_by_date', start_date, end_date)
    self.historico_gastos_list_copy.items = income
    self.plot_2.figure = self.create_income_plot(income)

  def historico_gastos_datepicker_change(self, **event_args):
    """This method is called when the date is changed"""
    self.load_expenses()

  def historico_receitas_datepicker_copy_change(self, **event_args):
    """This method is called when the date is changed"""
    self.load_income()

  def create_expense_plot(self, expenses):
    expenses_by_month = {}
    for expense in expenses:
      month = expense['date'].strftime("%Y-%m")
      if month not in expenses_by_month:
        expenses_by_month[month] = 0
      expenses_by_month[month] += expense['value']
    
    return go.Bar(
      x=list(expenses_by_month.keys()),
      y=list(expenses_by_month.values()),
      name="Expenses"
    )

  def create_income_plot(self, income):
    income_by_month = {}
    for inc in income:
      month = inc['date'].strftime("%Y-%m")
      if month not in income_by_month:
        income_by_month[month] = 0
      income_by_month[month] += inc['value']

    fig = go.Figure(
      [
        go.Bar(
          x=list(income_by_month.keys()),
          y=list(income_by_month.values()),
          name="Income"
        )
      ]
    )
    return fig
