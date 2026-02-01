from ._anvil_designer import ItemClinicaTemplateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemClinicaTemplate(ItemClinicaTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_nome.text = self.item['nome']
    self.label_codinome.text = self.item['codinome']
    self.label_total.text = f"R$ {self.item['total']}"

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('delete_client', self.item.get_id())
    self.parent.raise_event('x-refresh-data')

  def button_edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
