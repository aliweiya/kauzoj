#!/usr/bin/env python
import os, calendar
# import yaml

template = ""
with open("assets/scripts/caltemplate.yml",'r') as t:
    template = t.read()
    # template = yaml.load(t.read())

def genday(year,month,day):
    dirpath = "_data/{}/{}/".format(year,month)
    filepath = dirpath + "{}.yml".format(day)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    if not os.path.isfile(filepath):
        with open(filepath,'w+') as f:
            f.write(template)
            # f.write(yaml.dump(template))
def genmonth(year,month):
    maxday = calendar.monthrange(year,month)[1]
    for day in range(1,maxday+1):
        genday(year,month,day)

def genyear(year):
    for month in range(1,13):
        genmonth(year,month)

if __name__ == "__main__":
    genyear(2017)
