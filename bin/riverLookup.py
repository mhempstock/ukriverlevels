
import urllib2
import json
import csv
import sys, os
import time
import traceback
from multiprocessing.pool import ThreadPool as Pool
# from multiprocessing import Pool

pool_size = 20  # your "parallelness"
pool = Pool(pool_size)

stations=[]


def worker(i):

    try:
        if i.get('@id'):
            sdata = urllib2.urlopen(i['@id'])
            station = json.load(sdata)
            lat = station.get('items').get('lat')
            lon = station.get('items').get('long')
            stationReference = station.get('items').get('stationReference')
            label = station.get('items').get('label')
            typicalRangeHigh = station.get('items').get('stageScale',{}).get('typicalRangeHigh','unknown')
            typicalRangeLow = station.get('items').get('stageScale',{}).get('typicalRangeLow','unknown')    
        else:
            typicalRangeHigh="unknown"
            typicalRangeLow="unknown"
            
        town = i.get('town')
        riverName = i.get('riverName')
        stations.append({"station" : stationReference,"town": town,"riverName":riverName, "label":label, "lat":lat,"lon" :lon ,"typicalRangeHigh" :typicalRangeHigh ,"typicalRangeLow" :typicalRangeLow })
    except Exception, err:
        print(traceback.format_exc())


result_objs = []  
path = os.path.dirname(os.path.realpath(sys.argv[0]))+"/../lookups/river.csv"
print path
stations=[]
data = urllib2.urlopen("http://environment.data.gov.uk/flood-monitoring/id/stations")
datadict = json.load(data)
for i in datadict['items']:
    result_objs.append(pool.apply_async(worker, (i,)))
    
    
  
while True:
    incomplete_count = sum(1 for x in result_objs if not x.ready())

    if incomplete_count == 0:
        print "All done"
        break

    print str(incomplete_count) + " Tasks Remaining"
    time.sleep(10)

pool.close()
pool.join()



keys = keys = ["'station['items']", ]
keys = stations[0].keys()
with open(path, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(stations)
