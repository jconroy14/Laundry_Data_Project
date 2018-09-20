import psycopg2
import os
from math import trunc
from datetime import datetime
import csv

# define constants
DATABASE_URL = 'postgres://xjmgzqbovystmz:b59b93d8d13c724a530425e1e74b603b8ce3f7a2e56c98caa0156e7c7f5ca97e@ec2-107-22-221-60.compute-1.amazonaws.com:5432/djo19060qdtmp'
TOTAL_WASHERS = 5 #Used to be 5, switch to 4 at time stamp 1536445525
# Back to 6 from 1536923707 to 1536928494, back to 5 after (1536929097)
TOTAL_DRYERS = 8

dayOfWeek={
    'Monday':'9/3/2018 ', #arbitrary monday chosen so that Excel does not split mondays-data into deeper chronological order
    'Tuesday':'9/4/2018 ',
    'Wednesday':'9/5/2018 ',
    'Thursday':'9/6/2018 ',
    'Friday':'9/7/2018 ',
    'Saturday':'9/8/2018 ',
    'Sunday':'9/9/2018 '
}

# open data.csv as read-only and find last data previously recorded in csv
dataFile = open('data.csv','r')
previousData = list(csv.reader(dataFile))
lastTimeRecorded = previousData[len(previousData)-1][0]
dataFile.close()

# open connection to database and get the new data
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute("SELECT * FROM dataTable WHERE theTime>%s;",(lastTimeRecorded,))
data = cur.fetchall()
print(data)

conn.commit()
cur.close()
conn.close()

# append the new data to the file
dataFile = open('data.csv','a+')
for elementSet in data:
    timeInHours = datetime.fromtimestamp(elementSet[0]).strftime("%H:%M") #get time in format hh:mm
    weekday = dayOfWeek[datetime.fromtimestamp(elementSet[0]).strftime("%A")]
    timeInWeekdays = weekday+timeInHours; #get time in format ddd hh:mm
    dataFile.write('\n'+str(elementSet[0])+','+timeInHours+','+timeInWeekdays+','+str(TOTAL_WASHERS-elementSet[1])+','+str(TOTAL_DRYERS-elementSet[2]))
dataFile.close()
