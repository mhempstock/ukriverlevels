import urllib2
import json
import pickle
import os.path
script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))



def getrivers():
    data = urllib2.urlopen("http://environment.data.gov.uk/flood-monitoring/id/measures")
    datadict = json.load(data)
    riverlevels=[]
    for i in datadict['items']:
        try:
            riverlevels.append(i['stationReference']+'$%^%'+i['parameterName']+'$%^%'+i['latestReading']['dateTime']+'$%^%'+i['notation']+'$%^%'+str(i['latestReading']['value'])+'$%^%'+i['unitName'])

        except Exception:
            pass
    return riverlevels

rivers = getrivers()
newvalues=set(rivers)

oldvalues=set()
oldvaluelist = []
try:
    with open(script_dirpath+'/scratch', 'rb') as f:
        oldvaluelist = (pickle.load(f))
except Exception:
    pass
oldvalues = set(oldvaluelist)


with open(script_dirpath+'/scratch', 'wb') as f:
    pickle.dump(rivers, f)



toLog = newvalues.difference(oldvalues)
for v in toLog:
    station,parameterName,dateTime,notation,value,unit = v.split('$%^%')
    print "%s station=\"%s\" parameterName=\"%s\" notation=\"%s\" value=%s unit=%s" % (dateTime,station,parameterName,notation,value,unit)

