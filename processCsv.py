import pandas as pd
from math import trunc

BINS_PER_DAY = 24
MINUTES_IN_DAY = 1440

# open csv file and read out time and washers lists
dataSheet = pd.read_csv('/Users/jonathanconroy/Documents/laundryDataProject/data.csv')
timeInHours = dataSheet['TimeInHours']
washers = dataSheet['Washers Used']
dryers = dataSheet['Dryers Used']

# create a dictionary that associates a time (in minutes since 00:00) with the number of washers in use
washerDict = dict()
dryerDict = dict()
for i in range(0,len(washers)):
    currTime = int(timeInHours[i][-2:]) + int(timeInHours[i][:-3])*60 #currentTimeInMinutes
    if(currTime in washerDict):
        washerDict[currTime] = washerDict[currTime] + washers[i]
        dryerDict[currTime] = dryerDict[currTime] + dryers[i]
    else:
        washerDict[currTime] = [washers[i]]
        dryerDict[currTime] = [dryers[i]]
print(washerDict)
print(dryerDict)
# create a dictionary that associates each minute in the day with a washer number, relying on the last known washer number
minutesDict = dict.fromkeys(range(0,MINUTES_IN_DAY))
currWasherTime = min(washerDict.keys()) #start with the closest washer number to 00:00
for minute in range(0,MINUTES_IN_DAY):
    if(minute in washerDict):
        currWasherTime = minute
    minutesDict[minute] = {'washers':washerDict[currWasherTime],'dryers':dryerDict[currWasherTime]}
print('minutesDict' + str(minutesDict))
# get the data into bins that contain the average washer number
binSize = MINUTES_IN_DAY/BINS_PER_DAY
avgWashersInBins = [0] * BINS_PER_DAY
avgDryersInBins = [0] * BINS_PER_DAY
print(minutesDict)
for minute,data in minutesDict.items():
    avgWasherNumAtMinute = sum(data['washers'])/len(data['washers'])
    avgDryerNumAtMinute = sum(data['dryers'])/len(data['dryers'])
    binIndex = int(trunc(minute/binSize))
    avgWashersInBins[binIndex] = avgWashersInBins[binIndex] + avgWasherNumAtMinute/binSize
    avgDryersInBins[binIndex] = avgDryersInBins[binIndex] + avgDryerNumAtMinute/binSize

print(avgWashersInBins)
print(avgDryersInBins)

#print the data in a new csv file
newDataFile = open('processedData.csv','w+')
newDataFile.write('Time,Washers Used,,Time,Dryers Used\n')
for binNum in range(0,BINS_PER_DAY):
    # find the timestamp and washerNumber for each bin and write it to the new file
    timeInMinutes = binSize*binNum
    timeStamp = str(trunc(timeInMinutes/60)) + ':' + str(timeInMinutes%60)
    washerNum = avgWashersInBins[binNum]
    dryerNum = avgDryersInBins[binNum]
    newDataFile.write(timeStamp + ',' + str(washerNum)+',,' + timeStamp + ',' + str(dryerNum)+'\n')
newDataFile.close()
