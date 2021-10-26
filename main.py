from PLCreader import PLCreader 
from SQLwriter import SQLwriter
import time

#IPs not static and needs to be manually checked for each new session 
### PLC parameters ### 
plc_ip = '10.67.92.48'
rack = 0
slot = 1
db_nr = 1

### SQL server parameters ###
sql_ip= '10.67.92.47,49680' 
database = 'TestDB' 
table = 'demo_table'
username = 'TestUser' 
password = 'test123' 

def main():
    w = SQLwriter(sql_ip,database,table,username,password)
    r = PLCreader(plc_ip,rack,slot,db_nr)

    while(True):    
        names, values = r.read()
        w.write(names,values)
        print(values)
        time.sleep(1)


if __name__ == '__main__':
        main()