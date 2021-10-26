import snap7
from snap7 import util
from datetime import datetime
import numpy as np
import pandas as pd

### Vital TIAporta configuration ###
# Data block properties -> optimized block access = off
# CPU properties -> Permit access with PUT/GET com. = on

#Defining size in byte for each relevant datatype.
REAL_SIZE = 4
BOOL_SIZE = 1
DTL_SIZE = 12
COL_NAMES = ['Name','Data type','Offset']

class PLCreader:
    def __init__(self,ip,rack,slot,db_nr):
        self.client = snap7.client.Client()
        self.rack = rack
        self.ip = ip
        self.slot = slot
        self.db_nr = db_nr
        self.values = []
        self.names = []    

        self.client.connect(self.ip,self.rack,self.slot)

        self.df = pd.read_csv('DBconfig.csv', header = None)
        self.df.columns = COL_NAMES

        for index, row in self.df.iterrows():
            data_type = row['Data type']
            if data_type == "Bool":
                self.df.loc[index,'Size'] = BOOL_SIZE
            if data_type == "Real":
                self.df.loc[index,'Size'] = REAL_SIZE
            elif data_type == "DTL":
                self.df.loc[index,'Size'] = DTL_SIZE

    def read(self):
        self.getData()
        return self.names, self.values

    def getData(self):    
        self.values.clear()
        self.names.clear()
        
        for index, row in self.df.iterrows():
            offset = int(row['Offset'])
            size = int(row['Size'])    
            buffer = self.client.read_area(snap7.types.Areas.DB, self.db_nr, offset, size)
            if row['Data type'] == "Bool":
                value = util.get_bool(buffer,0,0)
                #print(value)
            if row['Data type'] == "Real":
                value = util.get_real(buffer,0)
                #print(value)
            if row['Data type'] == "DTL":
                #value = util.get_dt(buffer,0)
                #this is cheeting, could not parse DTL to something human readable.
                value = datetime.now()

            self.values.append(value)
            self.names.append(row['Name'])

def main():
    ### PLC parameters ### 
    plc_ip = '10.67.92.48'
    rack = 0
    slot = 1
    db_nr = 1
    r = PLCreader(plc_ip,rack,slot,db_nr)
    print(r.read())

if __name__ == '__main__':
        main()