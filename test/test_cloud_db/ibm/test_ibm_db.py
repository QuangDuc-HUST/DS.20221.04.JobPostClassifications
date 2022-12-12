import ibm_db 
import json
import time


dsn_hostname = "2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud" 
dsn_uid = "ycd08148"        
dsn_pwd = "oQKl88WlZOqJuLbN"      

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"            
dsn_port = "30756"                
dsn_protocol = "TCPIP"            
dsn_security = "SSL" 

f = open('./modeling/dw.sql', 'r')
dw_sql = f.readlines()
dw_sql = ''.join(dw_sql).strip().split(';')

job_sql = dw_sql[0]
# print(job_sql)

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)

    stmt = ibm_db.exec_immediate(conn, job_sql)
    stmt = ibm_db.exec_immediate(conn, dw_sql[1])

    start = time.time()
    c = open('./processing/staging/job/job.json', 'r')
    c = json.load(c)

    err = []

    for i in c:
        # print("INSERT INTO {} ({}) VALUES ( ".format('job', ','.join(i.keys())) + ",".join(["'" + str(i).replace("'", '"') + "'" for i in i.values()]) + ");")
        try:
            
            query = "INSERT INTO {} ({}) VALUES ( ".format('job', ','.join([v for v in i.keys() if str(i[v]) != ''])) + ",".join(["'" + str(i).replace("'", '"') + "'" for i in i.values() if str(i) != '']) + ");"
            # print(query)
            ibm_db.exec_immediate(conn, query)
        except Exception as e1:
            err.append(i)
            print(e1)
            break

except Exception as e:
    print(e)
    # print ("Unable to connect: ", ibm_db.conn_errormsg() )
finally:
    end = time.time()
    print(end - start)

    f =  open('./err.json', 'w')
    json.dump(err, f)

