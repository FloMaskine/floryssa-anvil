from ._anvil_designer import MenuTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..PainelPrincipal import PainelPrincipal
from ..Clinica import Clinica
from ..GastosMes import GastosMes
from ..Historicos import Historicos
from ..Graficos import Graficos

#This is your startup form. It has a sidebar with navigation links and a content panel where page content will be added.
class Menu(MenuTemplate):
  def __init__(self, form_to_open=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #Present users with a login form with just one line of code:
    #anvil.users.login_with_form()
 
    #Set the Plotly plots template to match the theme of the app
    Plot.templates.default = "rally"
    #When the app starts up, the PainelPrincipal form will be added to the page
    if form_to_open:
      self.column_panel_1.add_component(form_to_open)
    else:
      self.column_panel_1.add_component(PainelPrincipal())

  def historico_geral_menu_link_button_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Menu', form_to_open=Historicos())

  def graficos_gerais_menu_link_button_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Menu', form_to_open=Graficos())

  def gastos_mes_menu_link_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Menu', form_to_open=GastosMes())

  def signout_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()
    open_form('Logout')

  def clinica_menu_link_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Menu', form_to_open=Clinica())

  def painel_principal_menu_link_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Menu', form_to_open=PainelPrincipal())
