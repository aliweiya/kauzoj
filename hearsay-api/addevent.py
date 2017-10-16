from gencal import *

def addevent():
    datestring = raw_input("Enter yyyy/mm/dd: ")
    year, month, day = datestring.split("/")
    genday(year,month,day)
    regionstring = raw_input("Enter region: ")
    """
    open yaml, insert item into region string
    """
    eventstring = raw_input("What's the event?: ")
    sourcestring = raw_input("What's your source?: ")
