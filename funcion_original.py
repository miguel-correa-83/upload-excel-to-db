import os
import pandas as pd
import pymssql

#  Parámetros de conexión al SQL Server
sql_server = "localhost"
sql_database = "master"
sql_username = "sa"
sql_password = "jhf80DD%80F6g"

# Crear conexión
conn = pymssql.connect(server=sql_server, user=sql_username, password=sql_password, database=sql_database, charset='UTF-8')

cursor = conn.cursor()

file_path = './files/Informe STAFF SEM 41.xlsx'
# Usar openpyxl v3.0.10
df = pd.read_excel(file_path, dtype=str, engine="openpyxl", sheet_name="Status C de A", skiprows=1)
df = df.where(pd.notna(df), None)
df.rename(columns={'Fecha inicio de revisión': 'Fecha_Inicio_de_Revision'}, inplace=True)
df.rename(columns={'Dotación': 'Dotacion'}, inplace=True)
df.rename(columns={'N° de revisión': 'Num_de_Revision'}, inplace=True)
df.rename(columns={'% avance  C de A  Semana 41': 'Pje_Avance_C_de_A_Semana_41'}, inplace=True)



table_name = 'Informe_STAFF_SEM_41_Status_C_de_A'
# Generate the INSERT INTO statement with square brackets around column names
insert_sql = f"INSERT INTO {table_name} ([{'], ['.join(df.columns)}]) VALUES ({', '.join(['%s'] * len(df.columns))})"

# Iterate through DataFrame rows and insert them into the SQL Server table
for index, row in df.iterrows():
    values = tuple(row)
    cursor.execute(insert_sql, values)


conn.commit()

# Close the cursor
cursor.close()
