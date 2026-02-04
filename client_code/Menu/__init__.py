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
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #Present users with a login form with just one line of code:
    #anvil.users.login_with_form()
 
    #Set the Plotly plots template to match the theme of the app
    Plot.templates.default = "rally"
    #When the app starts up, the PainelPrincipal form will be added to the page
    self.column_panel_1.add_component(PainelPrincipal())
    self.painel_principal_menu_link_button.background = app.theme_colors['Primary Container']
    
  def reset_links(self):
    self.painel_principal_menu_link_button.background = "transparent"
    self.clinica_menu_link.background = "transparent"
    self.gastos_mes_menu_link_button.background = "transparent"
    self.historico_geral_menu_link_button.background = "transparent"
    self.graficos_gerais_menu_link_button.background = "transparent"

  def historico_geral_menu_link_button_click(self, **event_args):
    """This method is called when the link is clicked"""
    #Clear the content panel and add the wanted Form
    self.column_panel_1.clear()
    self.column_panel_1.add_component(Historicos())
    #Change the color of the link to indicate that the page has been selected
    self.reset_links()
    self.historico_geral_menu_link_button.background = app.theme_colors['Primary Container']

  def graficos_gerais_menu_link_button_click(self, **event_args):
    """This method is called when the link is clicked"""
    #Clear the content panel and add the Reports Form
    self.column_panel_1.clear()
    self.column_panel_1.add_component(Graficos())
    #Change the color of the link to indicate that the page has been selected
    self.reset_links()
    self.graficos_gerais_menu_link_button.background = app.theme_colors['Primary Container']

  def gastos_mes_menu_link_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_1.clear()
    self.column_panel_1.add_component(GastosMes())
    self.reset_links()
    self.gastos_mes_menu_link_button.background = app.theme_colors['Primary Container']

  def signout_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.users.logout()
    open_form('Login')

  def clinica_menu_link_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_1.clear()
    self.column_panel_1.add_component(Clinica())
    self.reset_links()
    self.clinica_menu_link.background = app.theme_colors['Primary Container']

  def painel_principal_menu_link_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.column_panel_1.clear()
    self.column_panel_1.add_component(PainelPrincipal())
    self.reset_links()
    self.painel_principal_menu_link_button.background = app.theme_colors['Primary Container']