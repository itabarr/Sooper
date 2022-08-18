import pyodbc
import xlrd
import xml.etree.ElementTree as ET

print("Connecting..")

server = 'database-1.ccod0bjmjgoj.eu-west-2.rds.amazonaws.com,1433'
database = 'MyFirstDB'
username = 'admin'
password = 'BJQwqieiUAJzTWqunGG7'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';uid='+username+';pwd='+ password)

cursor = cnxn.cursor()

#Sample select query
query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
df = cursor.execute(query)
print(df)
print("DB Connected..")

# Get XMLFile
XMLFilePath = open(r'C:\Users\as\Sooper\SeleniumDownload\Price7290027600007-001-202208181900.xml' , encoding="utf8")
x = ET.parse(XMLFilePath)# Updated Code line

x = x.getroot()
with open("FileName", "wb") as f:      # Updated Code line
    f.write(ET.tostring(x))         # Updated Code line

# Create Table in DB
CreateTable = """
create table test.dbo.TEMP
(

 XBRLFile XML

)
"""

# execute create table
cursor = cnxn.cursor()
try:
    cursor.execute(CreateTable).fetchall()
    cnxn.commit()
except pyodbc.ProgrammingError:
    pass
print("Table Created..")

InsertQuery = """
INSERT INTO test.dbo.TEMP (
    XBRLFile
) VALUES (?)"""

# Assign values from each row
values = ET.tostring(x) # Updated Code line

# Execute SQL Insert Query
cursor.execute(InsertQuery, values)

# Commit the transaction
cnxn.commit()

# Close the database c