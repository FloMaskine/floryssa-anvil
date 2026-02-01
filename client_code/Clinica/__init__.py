from ._anvil_designer import ClinicaTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ItemClinicaTemplate import ItemClinicaTemplate

class Clinica(ClinicaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_clients()
    self.repeating_panel_pacientes_particulares.set_event_handler('x-refresh-data', self.load_clients)
    self.repeating_panel_clinicas.set_event_handler('x-refresh-data', self.load_clients)

  def load_clients(self, **event_args):
    clients = anvil.server.call('get_clients')
    particulares = [client for client in clients if client['categoria'] == 'Particular']
    clinicas = [client for client in clients if client['categoria'] == 'Clinica']
    self.repeating_panel_pacientes_particulares.items = particulares
    self.repeating_panel_clinicas.items = clinicas

  def button_add_client_click(self, **event_args):
    """This method is called when the button is clicked"""
    valor_sessao = float(self.text_box_valor_sessao_clinica.text)
    sessoes_mes = int(self.text_box_sessoes_mes_clinica.text)
    client_data = {
      'nome': self.text_box_nome_clinica.text,
      'codinome': self.text_box_codinome_clinica.text,
      'cpf-cnpj': self.text_box_cpf_cnpj_clinica.text,
      'valor-por-sessao': valor_sessao,
      'sessoes-mes': sessoes_mes,
      'sessoes-pagas': 0,
      'total': valor_sessao * sessoes_mes,
      'categoria': self.drop_down_categoria_clinica.selected_value,
      'status': True
    }
    anvil.server.call('add_client', client_data)
    self.load_clients()
    self.text_box_nome_clinica.text = ""
    self.text_box_codinome_clinica.text = ""
    self.text_box_cpf_cnpj_clinica.text = ""
    self.text_box_valor_sessao_clinica.text = ""
    self.text_box_sessoes_mes_clinica.text = ""
