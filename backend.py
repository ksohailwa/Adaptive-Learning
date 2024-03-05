

import urllib.parse
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from sqlalchemy import create_engine


#DATABASE CONNECTION

params = urllib.parse.quote_plus(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:adaptive-learning-server.database.windows.net,1433;Database=adaptive_learning_db;Uid=superadmin;Pwd=Poorpassword@2024;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)
connection = engine_azure.connect()
print("Connection successful !!!!")



# callback function to retrieve data from database query

def retrieve_data(query):

      result = connection.execute(query)
      df = pd.DataFrame(result.fetchall(), columns=result.keys())
      print("!!! df retrieved values:", df)
      return df




