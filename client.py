import sqlite3


conn = sqlite3.connect("clientDB.db")
c = conn.cursor()

class getClientInfo:
    
    def numClients():
        

        numClients = 0

        sql = "SELECT * FROM clientInfo"

        for rows in c.execute(sql):
            numClients += 1

        #subtract 1 for test client in original create of db
        numClients-=1
        conn.commit()
        

        
        

        return numClients

    def getClientID(fname, mname, lname):

        
        count = 0
        for row in (c.execute("SELECT cliNum FROM clientInfo WHERE firstName = ? AND middleName = ? AND lastName = ?", (fname, mname, lname))):
            r=row
            count+=1
        s=r[0]

        return s

    #printer function is for troubleshooting the db
    #prints all data to console
    def printer():
        for line in c.execute("SELECT * FROM clientInfo"):
            print(line)

        
