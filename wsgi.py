from joshua.app import App
from joshua.request import Request
from joshua.request import Request
from joshua.response import HttpResponse
from joshua.router import Path
from wsgiref.simple_server import make_server
from aludbms import query
import json
port = 8080
app = App()
tomorrow=""
today=""
yesterday=""
def process_dates():
    global yesterday
    global today
    global tomorrow
    from datetime import datetime, timedelta
    presentday_cal = datetime.now()
    yesterday_cal = presentday_cal - timedelta(1)
    tomorrow_cal = presentday_cal + timedelta(1)
    yesterday=yesterday_cal.strftime('%Y-%m-%d').replace("-","")
    today=presentday_cal.strftime('%Y-%m-%d').replace("-","")
    tomorrow=tomorrow_cal.strftime('%Y-%m-%d').replace("-","")

process_dates()

def isdigit(num):
    try:
        int(num)
        return True
    except:
        return False

def generror(errorstr):
    return str(open("joshua/pretty.html").read().replace("replaceme", errorstr).replace("#298bf5", "#000000"))

def genmsg(msgstr):
    return str(open("joshua/pretty.html").read().replace("Error replaceme", msgstr))

def render_template(name):
    return open(name).read()

def today(request: Request):
    process_dates()
    date=request.query_string.split("=")[1]
    if date==today or date==yesterday or date==tomorrow:
        return HttpResponse(request, '['+(str(query.get("puzzles", date).values())[13:-2]).replace("'",'"')+']')
    else:
        return HttpResponse(request, generror("Invalid Date!"))

def playtest(request: Request):
    date=request.query_string.split("=")[1]
    return HttpResponse(request, (str(query.get("puzzles", date).values())[13:-2]))

def is_ascending(check: list):
    last=""
    for x in check:
        if len(last)<len(x):
            last=x
        else:
            return False
    return True

def admin(request: Request):
    return HttpResponse(request, render_template("admin.html"))

def add(request: Request):
    puzzarr=(request.query_string.split("=")[1]).replace("%22",'"').replace("%27","'")
    try:
        a=json.loads(puzzarr)
        if str(type(a))=="<class 'list'>":
            date=a[0]
            keyword=a[-1]
            if keyword!="test":
                return HttpResponse(request, generror("Unauthorized Access"))
            parr=a
            del parr[0]
            del parr[-1]
            if is_ascending(parr):
                pass
            else:
                return HttpResponse(request, generror("Wrong word formatting"))
            if isdigit(date)==True:
                if query.add("puzzles", {date:parr}):
                    return HttpResponse(request, genmsg("Puzzle Successfully Added!"))
                else:
                    return HttpResponse(request, generror("Puzzle Could Not Be Added"))
            else:
                print(date)
                return HttpResponse(request, generror("Missing Date Input"))
        else:
            return HttpResponse(request, generror("Wrong Format"))
    except Exception as e:
        return HttpResponse(request, generror("JSON Parsing Failed"))

def errorpage(request: Request):
    return HttpResponse(request, generror(request.query_string.split("=")[1]))

routes = [
    Path('/puzzle', today),
    Path('/playtest', playtest),
    Path('/admin', admin),
    Path('/add', add),
    Path('/error', errorpage),
]

app.set_routes(routes)
serverh = make_server("127.0.0.1", port, app)
print('Server Listening On Port ',port)
print('Printing Log')
serverh.serve_forever()
input("Press enter to proceed...")