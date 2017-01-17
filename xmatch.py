# xmatch.py
# Code to check if any Gaia Alerts lie within the K2 footprint
#
# Morgan Fraser
# University College Dublin 
# morgan.fraser_at_ucd.ie
#
# v1.0 16 Jan 2017

import csv, sys
import json
from datetime import datetime as dt

csv.field_size_limit(sys.maxsize)

# This array has start and end dates for the K2 campaigns
datearray= [[["c0"],["2014-03-08"],["2014-05-27"]],   
[["c1"],["2014-05-30"],["2014-08-21"]],   
[["c2"],["2014-08-23"],["2014-11-13"]],
[["c3"],["2014-11-14"],["2015-02-03"]],   
[["c4"],["2015-02-07"],["2015-04-23"]],   
[["c5"],["2015-04-27"],["2015-07-10"]],   
[["c6"],["2015-07-14"],["2015-09-30"]],   
[["c7"],["2015-10-04"],["2015-12-26"]],   
[["c8"],["2016-01-03"],["2016-03-23"]],  
[["c9"],["2016-04-21"],["2016-07-01"]],   
[["c10"],["2016-07-06"],["2016-09-20"]],   
[["c11"],["2016-09-24"],["2016-12-08"]],   
[["c12"],["2016-12-15"],["2017-03-04"]],   
[["c13"],["2017-03-08"],["2017-05-27"]],   
[["c14"],["2017-05-31"],["2017-08-19"]],   
[["c15"],["2017-08-23"],["2017-11-20"]],  
[["c16"],["2017-12-07"],["2018-02-25"]]] 


# Read alerts into list
# Note that the alerts.csv file is the one downloaded from gsaweb, but with the lines trimmed
# as some of the comment fields were too long
alerts = []
with open('alerts2.csv', 'rb') as alerts_file:
    alerts_list = csv.reader(alerts_file, quotechar='#')
    for row in alerts_list:
        alerts.append(row)

# Load K2 footprints
# k2-footprint downloaded from https://keplerscience.arc.nasa.gov/k2-fields.html
footprint_dictionary = json.load(open("k2-footprint.json"))

print "searching through "+str(len(alerts))+" alerts..."

# Looping over campaign and channel
for campaign in ["c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13","c14","c15","c16"]:
    print "Campaign ", campaign, ":"
    for channel in range(0,100):
# Check that channel can be loaded from dictionary
        try:
            current_channel = footprint_dictionary[str(campaign)]["channels"][str(channel)]
        except KeyError:
            continue
        else:
# Find min and max ra, dec of this channel footprint
            ra_array = []
            dec_array = []
            for i in range(0,3):
                ra_array.append(current_channel["corners_ra"][i])
                dec_array.append(current_channel["corners_dec"][i])
            ra_min=min(ra_array)
            ra_max=max(ra_array)
            dec_min=min(dec_array)
            dec_max=max(dec_array)     

# Now loop over list of alerts       
            for row in range(0,len(alerts)-1):
# Check if the alert is inside channel region
                if float(alerts[row][2])>ra_min and float(alerts[row][2])<ra_max and float(alerts[row][3])>dec_min and float(alerts[row][3])<dec_max:
#                    print alerts[row][0], alerts[row][1], alerts[row][2], alerts[row][3], campaign, channel
# Check what dates the alert was found on                    
                    for j in range(0,len(datearray)):
                        observed_campaign= ' '.join(datearray[j][0]) 
                        if observed_campaign==campaign:
# Read in start and end date of campaign from array
                            start_date = dt.strptime(' '.join(datearray[j][1]), "%Y-%m-%d")
                            end_date = dt.strptime(' '.join(datearray[j][2]), "%Y-%m-%d")
                            sn_time = dt.strptime(alerts[row][1][:10], "%Y-%m-%d")
# Check if SN was discovered early
                            tdelta_start = start_date - sn_time
                            if tdelta_start.total_seconds()<(180*24*3600) and tdelta_start.total_seconds()>0:
                                print "SN discovered less than 6 months before start of K2 campaign", alerts[row][0], alerts[row][1], alerts[row][2], alerts[row][3], campaign, channel
# Check if SN was discovered late                                
                            tdelta_end = sn_time - end_date
                            if tdelta_end.total_seconds()<(180*24*3600) and tdelta_end.total_seconds()>0:
                                print "SN discovered less than 6 months after end of K2 campaign", alerts[row][0], alerts[row][1], alerts[row][2], alerts[row][3], campaign, channel
# Check if SN was discovered during K2 campaign                        
                            if sn_time<end_date and sn_time>start_date:
                                print "SN discovered within Kepler season", alerts[row][0], alerts[row][1], alerts[row][2], alerts[row][3], campaign, channel
                                