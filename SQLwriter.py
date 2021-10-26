import pyodbc

class SQLwriter:

    def __init__(self,ip,db,table,user,pw):
        self.server = ip
        self.database = db
        self.username = user
        self.table = table              
        self.cn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+pw)
        self.cur = self.cn.cursor()
        
    def createString(self, names):
        name_string = "("
        s_string = "("
        for i in range(len(names)):
            name_string = name_string + str(names[i]) + ", "
            s_string = s_string + "?,"
            
        name_string = name_string[:-2] + ")"
        s_string = s_string[:-1]+ ")" 

        command_string ="INSERT INTO " + self.table + " " + name_string + " VALUES " + s_string       

        return command_string
    
        
    def write(self, names, values):

        if not(len(names)==len(values)):
            raise Exception("value and names vectors must be same length")
        
        command_string = self.createString(names)
        self.cur.execute(command_string, values)
        self.cn.commit()
        

test_names = ['Sine1', 'Sine2']
test_values = [-1.2982183694839478, -0.35004907846450806]

def main():
    ### SQL server parameters ###
    sql_ip= '10.67.92.47,49680' 
    database = 'TestDB' 
    table = 'demo_table'
    username = 'TestUser' 
    password = 'test123'
    w = SQLwriter(sql_ip,database,table,username,password)
    w.write(test_names,test_values)


    """"cur = cn.cursor()
    cur.execute("SELECT * FROM TestTable")
    for x in cur:
        print(x)    
    """

if __name__ == '__main__':
        main()