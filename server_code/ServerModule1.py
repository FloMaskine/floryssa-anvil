import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import plotly.graph_objects as go
from anvil.tables import app_tables
import anvil.server
import anvil.plotly_templates
import datetime

anvil.plotly_templates.set_default("rally_dark")

#<editor-fold desc="Dashboards">
#Return the contents of the Files data table. If this table included secure data, 
#we would only want to return the data that can be user visible
@anvil.server.callable
def return_table():
  return app_tables.files.search()

@anvil.server.callable
def return_data(year):
  #Your code to process and return data goes here
  if year == "2023":
    return [
      [11342, 11673, 12684, 12933, 13782, 13001, 13532, 13776, 14609, 15076, 15663, 15989], 
      [14331, 14887, 13520, 13021, 11000, 12956, 13451, 14805, 16004, 16599, 17885, 19053]
    ]
  elif year == "2022":
    return [
      [8695, 8704, 9201, 9554, 9760, 9963, 10003, 10889, 11073, 11992, 12743, 11221], 
      [12332, 12633, 13000, 13843, 12849, 12675, 13742, 14009, 14376, 14587, 15002, 14556]
    ]
  elif year == "2021":
    return [
      [5680, 5743, 5802, 6003, 6212, 7004, 6854, 6013, 6599, 7032, 7453, 7960, 8734], 
      [7832, 7945, 8432, 8049, 8775, 9321, 9674, 9900, 10342, 11483, 11954, 12511, 12030]
    ]

@anvil.server.callable
def return_bar_charts():
  #You can use any Python plotting library on the server including Plotly Express, MatplotLib, Seaborn, Bokeh
  fig = go.Figure(
    [
      go.Bar(
        y=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        x=[13, 21, 64, 119, 94],
        orientation='h',
        name="New Users"
        ),
      go.Bar(
        y=["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        x=[24, 35, 80, 250, 274],
        orientation='h',
        name="Existing Users"
      ),
    ]
  )
  
  fig.update_layout(
    barmode="stack",
  )
  return fig

@anvil.server.callable
def get_dashboard_data():
  today = datetime.date.today()
  current_month = today.strftime("%B")
  current_year = today.year

  total_income = sum([i['value'] for i in app_tables.income.search(month=current_month, year=current_year)])
  total_expenses = sum([e['value'] for e in app_tables.expenses.search(month=current_month, year=current_year)])

  # Fixed bills (contas_fixas)
  fixed_bills = app_tables.contas_fixas.search()
  total_fixed_bills = sum([b['valor'] for b in fixed_bills])
  paid_fixed_bills = sum([b['valor'] for b in fixed_bills if b['status']])
  remaining_fixed_bills = total_fixed_bills - paid_fixed_bills
  
  # Assuming 'dashboard' table stores account balances and control figures
  dashboard_row = app_tables.dashboard.get(saldo=q.not_(None)) # Get the first row, or adjust query as needed

  if dashboard_row:
    conta_flora = dashboard_row['conta-flora']
    conta_lary = dashboard_row['conta-lary']
    conta_pj = dashboard_row['conta-pj']
    falta_ganhar = dashboard_row['falta-ganhar']
    falta_pagar = dashboard_row['falta-pagar']
  else:
    # Default values if dashboard_row doesn't exist
    conta_flora = 0
    conta_lary = 0
    conta_pj = 0
    falta_ganhar = 0
    falta_pagar = 0

  return {
    'entradas_mes': total_income,
    'saidas_mes': total_expenses,
    'falta_ganhar': falta_ganhar, # This should be calculated based on clinica, but for now use dummy
    'falta_pagar': falta_pagar, # This should be calculated based on contas_fixas, but for now use dummy
    'conta_flora': conta_flora,
    'conta_lary': conta_lary,
    'conta_pj': conta_pj,
    'progresso_contas_pagas': (paid_fixed_bills / total_fixed_bills) * 100 if total_fixed_bills > 0 else 0
  }
#</editor-fold>

#<editor-fold desc="Gastos">
@anvil.server.callable
def add_expense(expense_data):
  app_tables.expenses.add_row(
    name=expense_data['name'],
    category=expense_data['category'],
    value=expense_data['value'],
    date=expense_data['date'],
    month=expense_data['date'].strftime("%B"),
    year=expense_data['date'].year
  )

@anvil.server.callable
def get_expenses(month, year):
  return app_tables.expenses.search(month=month, year=year)

@anvil.server.callable
def get_expenses_by_date(start_date, end_date):
  return app_tables.expenses.search(date=q.between(start_date, end_date))

@anvil.server.callable
def get_expenses_by_month(month, year):
  return app_tables.expenses.search(month=month, year=year)

@anvil.server.callable
def get_expenses_by_category(month, year):
  expenses = app_tables.expenses.search(month=month, year=year)
  categories = {}
  for expense in expenses:
    category = expense['category']
    if category not in categories:
      categories[category] = 0
    categories[category] += expense['value']
  return categories


@anvil.server.callable
def update_expense(expense_id, expense_data):
  row = app_tables.expenses.get_by_id(expense_id)
  row.update(
    name=expense_data['name'],
    category=expense_data['category'],
    value=expense_data['value'],
    date=expense_data['date']
  )

@anvil.server.callable
def delete_expense(expense_id):
  row = app_tables.expenses.get_by_id(expense_id)
  row.delete()
#</editor-fold>

#<editor-fold desc="Receitas">
@anvil.server.callable
def add_income(income_data):
  app_tables.income.add_row(
    description=income_data['description'],
    category=income_data['category'],
    value=income_data['value'],
    date=income_data['date'],
    month=income_data['date'].strftime("%B"),
    year=income_data['date'].year
  )

@anvil.server.callable
def get_income(month, year):
  return app_tables.income.search(month=month, year=year)

@anvil.server.callable
def get_income_by_date(start_date, end_date):
  return app_tables.income.search(date=q.between(start_date, end_date))

@anvil.server.callable
def get_income_by_month(month, year):
  return app_tables.income.search(month=month, year=year)

@anvil.server.callable
def delete_income(income_id):
  row = app_tables.income.get_by_id(income_id)
  row.delete()

@anvil.server.callable
def get_income_dashboard_data():
  today = datetime.date.today()
  current_month = today.strftime("%B")
  current_year = today.year

  total_income = sum([i['value'] for i in app_tables.income.search(month=current_month, year=current_year)])

  income_by_month = {}
  for i in app_tables.income.search():
    month_year = i['date'].strftime("%Y-%m")
    if month_year not in income_by_month:
      income_by_month[month_year] = 0
    income_by_month[month_year] += i['value']

  return {
    'total_income': total_income,
    'income_by_month': income_by_month
  }
#</editor-fold>

#<editor-fold desc="Clinica">
@anvil.server.callable
def add_client(client_data):
  app_tables.clinica.add_row(**client_data)

@anvil.server.callable
def get_clients():
  return app_tables.clinica.search()

@anvil.server.callable
def update_client(client_id, client_data):
  row = app_tables.clinica.get_by_id(client_id)
  row.update(**client_data)

@anvil.server.callable
def delete_client(client_id):
  row = app_tables.clinica.get_by_id(client_id)
  row.delete()
#</editor-fold>