from ._anvil_designer import IncomeMesTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class IncomeMes(IncomeMesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.date_picker_income.date = datetime.date.today()
    self.load_income()
    self.repeating_panel_income_mes.set_event_handler('x-refresh-data', self.load_income)

  def load_income(self, **event_args):
    month = self.date_picker_income.date.strftime("%B")
    year = self.date_picker_income.date.year
    self.repeating_panel_income_mes.items = anvil.server.call('get_income', month, year)

  def button_add_income_click(self, **event_args):
    """This method is called when the button is clicked"""
    income_data = {
      'description': self.text_box_description_income.text,
      'category': self.text_box_category_income.text,
      'value': float(self.text_box_value_income.text),
      'date': self.date_picker_income.date
    }
    anvil.server.call('add_income', income_data)
    self.load_income()
    self.text_box_description_income.text = ""
    self.text_box_category_income.text = ""
    self.text_box_value_income.text = ""

  def date_picker_income_change(self, **event_args):
    """This method is called when the date is changed"""
    self.load_income()