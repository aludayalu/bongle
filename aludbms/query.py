import json
import traceback
def get(dbname,query,contains=False):
    try:
        db=open((dbname+".aludb"),mode="r+")
    except:
        print("Error : False Database Name or Directory(Make sure the DB file is located in the same directory\nAnd do not include the extension along with the DB name.")
        return False
    dbcontents=dict(json.loads(db.read()))
    totallength=len(dbcontents["blocks"])
    res=""
    if totallength!=0:
        for i in range(totallength):
            for key in dbcontents["blocks"][i-1]:
                if key==query:
                    res=dict(dbcontents["blocks"][i-1])
                elif contains==True:
                    if query in key:
                        res=dict(dbcontents["blocks"][i-1])
            i+=1
        if res=="":
            return False
        else:
            return res
    else:
        return False

def add(dbname,query: dict):
    try:
        db=open((dbname+".aludb"),mode="r+",encoding = 'utf-8')
    except:
        print("Error : False Database Name or Directory(Make sure the DB file is located in the same directory\nAnd do not include the extension along with the DB name.")
        return False
    if get(dbname,str(query.keys())[12:-3])==False:
        dbcontents=dict(json.loads(db.read()))
        dbcontents["blocks"].append(query)
        db=open((dbname+".aludb"),"r+",encoding = 'utf-8')
        db.write(json.dumps(dbcontents))
        return True
    else:
        return False

def getviaindex(dbname,indexofitem):
    try:
        db=open((dbname+".aludb"),mode="r+")
    except:
        print("Error : False Database Name or Directory(Make sure the DB file is located in the same directory\nAnd do not include the extension along with the DB name.")
        return False
    dbcontents=dict(json.loads(db.read()))
    totallength=len(dbcontents["blocks"])
    res=""
    if totallength!=0:
        try:
            res=dbcontents["blocks"][indexofitem]
        except:
            traceback.print_exc()
            return False
        if res=="":
            return False
        else:
            return res
    else:
        return False

def getindex(dbname,query):
    try:
        db=open((dbname+".aludb"),mode="r+")
    except:
        print("Error : False Database Name or Directory(Make sure the DB file is located in the same directory\nAnd do not include the extension along with the DB name.")
        return False
    dbcontents=dict(json.loads(db.read()))
    totallength=len(dbcontents["blocks"])
    res=""
    if totallength!=0:
        try:
            return dbcontents["blocks"].index(query)
        except:
            traceback.print_exc()
            return False
        if res=="":
            return False
        else:
            return res
    else:
        return False