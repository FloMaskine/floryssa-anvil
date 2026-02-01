from ._anvil_designer import ItemTemplateTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate(ItemTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_description_gasto.text = self.item['description']
    self.label_valor_gasto.text = f"R$ {self.item['value']}"
    self.label_date_gasto.text = self.item['date'].strftime("%d/%m/%Y")