'''
Created on 29 Dec 2014

@author: martin
'''
import urllib2
import re
import time
import os
import os.path

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))





file = open(script_dirpath+'/rivers', 'r')
temp = [line[:-1] for line in file]
for river in temp:
    h = urllib2.urlopen("http://apps.environment-agency.gov.uk/river-and-sea-levels/120701.aspx?stationId="+river).readlines()

   
    for line in h:
        line = line.rstrip()
        norms = re.search('The typical river level range for this location is between (.+) metres and (.+) metres', line)
        current = re.search('river level at (.*) is (.*) metres',line)
        highest= re.search('The highest river level recorded at this location is (.+) metres and the river level reached (.+) metres on (.+)\.',line)

        if current:
            print time.strftime("%d/%b/%Y:%H:%M:%S %z") + ' location="' + current.group(1)+'" loccode="'+river+'" level="'+current.group(2)+'"'
        if norms:
            print 'lownorm="'+norms.group(1) +'" highnorm="' + norms.group(2) + '"'
        if highest: 
            print 'highestRecorded="' + highest.group(1) + '" recentHighest="' + highest.group(2) + '" recentHighestDate="' + highest.group(3) + '"'
