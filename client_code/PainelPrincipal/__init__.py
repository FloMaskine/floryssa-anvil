from ._anvil_designer import PainelPrincipalTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

class PainelPrincipal(PainelPrincipalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_dashboard_data()
    
  def load_dashboard_data(self):
    dashboard_data = anvil.server.call('get_dashboard_data')
    self.entradas_mes.text = f"R$ {dashboard_data['entradas_mes']:.2f}"
    self.saidas_mes.text = f"R$ {dashboard_data['saidas_mes']:.2f}"
    self.falta_ganhar.text = f"R$ {dashboard_data['falta_ganhar']:.2f}"
    self.falta_pagar.text = f"R$ {dashboard_data['falta_pagar']:.2f}"
    self.text_conta_flora.text = f"R$ {dashboard_data['conta_flora']:.2f}"
    self.text_conta_lary.text = f"R$ {dashboard_data['conta_lary']:.2f}"
    self.text_conta_pj.text = f"R$ {dashboard_data['conta_pj']:.2f}"

    self.grafico_contas_pagas.data = [
      go.Pie(
        labels=["Paid", "Remaining"],
        values=[dashboard_data['progresso_contas_pagas'], 100 - dashboard_data['progresso_contas_pagas']],
        hole=.5
      )
    ]
