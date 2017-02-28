import pyodbc

cnxn = pyodbc.connect('DSN=DenodoODBCa;PWD=admin;UID=admin;DATABASE=staging;')

print(cnxn)

cursor = cnxn.cursor()



cursor.execute('select * from staging.staging.statement')
# cursor.tables(catalog='staging')
row = cursor.fetchone()
if row:
    print(row)


cursor.execute('select * from staging.staging.statement')

from sqlalchemy import *
import sqlalchemy

url=sqlalchemy.engine.url.URL('DenodoODBCa', username='admin', password='admin', host='localhost', port=9996, database='staging', query=None)
print(url)
engine = create_engine(url)
metadata = MetaData()
# staging = Table('staging', metadata, autoload=True, autoload_with=engine)
# my_view = Table("some_view", metadata, autoload=True)
