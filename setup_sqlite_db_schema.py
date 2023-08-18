import sqlite3
import subprocess
import os 

# create database
conn = sqlite3.connect('ml_streamlit_application_data.db')


print('Database Created.\n')

# change permission
# subprocess.call(['sh', './create_sqlite_table.sh'])
print('Changing create_sqlite_table.sh permissions...')
os.system('chmod +x create_sqlite_table.sh')

# create table for model prediction
subprocess.run(['sh', './create_sqlite_table.sh'])