import properties
import mysql.connector
import properties

username = properties.mysql_user
passwd = properties.mysql_pass
hostname = properties.host
dbname = properties.db
plugin = properties.plugin
company = properties.co

conn = mysql.connector.connect(user=username,password=passwd,host=hostname,database=dbname, auth_plugin=plugin)
useTable = "use sec;"
useCursor = conn.cursor()
useCursor.execute(useTable)

tableHere = "select" 
create_table = "create table :coName ( dumbcolumn integer null);"
find_tables = "show tables;"

cursor = conn.cursor()
getTable = conn.cursor(prepared=True)

cursor.execute(find_tables)

tables = cursor.fetchall()

if len(tables) == 0:
    print(tables[0])
else:
    print ('Table not found, creating...')
    create_table = 'create table {}_filings ( dumbcolumn integer null);'.format(company)
    print(create_table)
    getTable.execute(create_table)
    conn.commit()
    print('Tables')
    cursor.execute(create_table)
    tables = cursor.fetchall()
    print(tables[0])

# conn.commit()

cursor.close()

conn.close()
