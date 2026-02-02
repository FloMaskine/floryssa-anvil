from ._anvil_designer import ItemIncomeTemplateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemIncomeTemplate(ItemIncomeTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_description_income.text = self.item['description']
    self.label_valor_income.text = f"R$ {self.item['value']}"
    self.label_date_income.text = self.item['date'].strftime("%d/%m/%Y")
    self.check_box_received.checked = self.item['nota_lancada']

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('delete_income', self.item.get_id())
    self.parent.raise_event('x-refresh-data')

  def check_box_received_change(self, **event_args):
    """This method is called when the check box is changed"""
    self.item['nota_lancada'] = self.check_box_received.checked

  def button_edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass