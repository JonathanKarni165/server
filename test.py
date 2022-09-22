import pyodbc
import pygame

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\yonat\OneDrive\Desktop\PythonWorkspace\ms access\Chat.accdb;')
cursor = conn.cursor()

cursor.execute('insert into clients values (?, ?, ?)', (3, 'conti', '1234'))
conn.commit()

