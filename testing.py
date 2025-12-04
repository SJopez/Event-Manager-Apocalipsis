import datetime as dt
from datetime import timedelta
from plot import get_duration, get_date
from utilities import *

def getInterval(end, index, jump, duration):
    ini = end + timedelta(index * jump + duration * (index - 1))
    end = ini + timedelta(duration)
    return (ini, end)

def verifyColission(l, r, jump, d1, d2, t, d3, d4):
    from event_manager import interception

    if interception(d1, d2, d3, d4):
        return True
    
    elif jump == "-":
        return False
    
    while l < r:
        mid = (l + r) // 2
        curr = getInterval(d2, mid, jump, t) 

        if interception(curr[0], curr[1], d3, d4):
            return mid
        elif curr[0] > d2:
            r = mid
        else:
            l = mid + 1
    
    return False

def dateFromEvent(event):
    di = event["fechaInicio"]
    df = event["fechaFin"]
    ti = event["tiempoInicio"]
    tf = event["tiempoFin"]

    ini = get_date(di[0], di[1], di[2], ti[0], ti[1])
    end = get_date(df[0], df[1], df[2], tf[0], tf[1])

    return (ini, end)

def createRecurrentEvent(event):
    duration = get_duration(event)
    running = readJson("running_events.json")
    jump = int(event["jump"])
    date = dateFromEvent(event)
    valid = True

    for e in running:
        currDate = dateFromEvent(e)

        if e["jump"] != "-" or verifyColission(1, 5000, jump, date[0], date[1], duration, currDate[0], currDate[1]):
            for r in e["recursos"]:
                type = r[0]
                total = get_one(type)["cantidad"]
                

    if valid:
        return (valid, None)

    