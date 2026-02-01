from ._anvil_designer import GastosMesTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class GastosMes(GastosMesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.date_picker_gasto.date = datetime.date.today()
    self.load_expenses()
    self.repeating_panel_gastos_mes.set_event_handler('x-refresh-data', self.load_expenses)

  def load_expenses(self, **event_args):
    month = self.date_picker_gasto.date.strftime("%B")
    year = self.date_picker_gasto.date.year
    self.repeating_panel_gastos_mes.items = anvil.server.call('get_expenses', month, year)

  def button_add_gasto_click(self, **event_args):
    """This method is called when the button is clicked"""
    expense_data = {
      'name': self.text_box_description_gasto.text,
      'category': self.text_box_category_gasto.text,
      'value': float(self.text_box_value_gasto.text),
      'date': self.date_picker_gasto.date
    }
    anvil.server.call('add_expense', expense_data)
    self.load_expenses()
    self.text_box_description_gasto.text = ""
    self.text_box_category_gasto.text = ""
    self.text_box_value_gasto.text = ""

  def date_picker_gasto_change(self, **event_args):
    """This method is called when the date is changed"""
    self.load_expenses()
