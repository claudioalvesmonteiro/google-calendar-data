'''
TEXT MINING OF ICS FILE FROM GOOGLE CALENDAR

Takes the ics file as input and 
export a CSV dataset with the informations
'''

# import modules
import pandas as pd
import datetime

file = 'claudiomonteirol.a@gmail.com.ics'

#================================#
# READ AND TRANSFORM ICS IN DICT
#================================#

def listToData(file):
    ''' opens a ics file as text,
        split text into events,
        split events into informations,
        select informations and append to
        to dictionary of lists to be transformed in
        pandas dataframe
    '''

    # read file as text
    file = open(file, 'r')
    cal = file.read()

    # break text in strings of events
    cal = cal.split('BEGIN:VEVENT')

    # break events in infos
    cal = [x.split('\n') for x in cal]

    # data as dictionary
    data = {'DTSTART': [],
            'DTEND': [],
            'UID': [], 
            'CREATED': [], 
            'LAST-MODIFIED': [], 
            'LOCATION': [], 
            'SEQUENCE': [], 
            'STATUS': [], 
            'SUMMARY': [],
            'TRANSP': []
    }

    # loop for appending the infos to dict columns
    for event in cal[1:]: # this hide the first element wich is not a event, but hides the local timezone too
        for info in event:
            for key, value in data.items():
                if key == 'SUMMARY':
                    if 'Alarm' not in info:
                        if key in info:
                            data[key].append(info)
                else:
                    if key in info:
                        data[key].append(info)
    # return data
    return data


# aply function to local file
data = listToData('claudiomonteirol.a@gmail.com.ics')

# transform dict in pd dataframe
dataset = pd.DataFrame(data)

# dataset head
dataset.head()

#==========================#
# CLEAN DATA
#==========================#

# split DSTART e DTEND in date,time columns each
def dateSelector(data, column, name):
    ''' takes a pandasDF and a column to split 
        the column rows into two columns
    '''
    # split rows of the target column into a list
    sere = []
    for row in column:
        split_row = row.split(':')
        sere.append(split_row[1])
    # split the list values in date and time and append informations
    year = []
    month = []
    day = []
    caldate =[]
    time = []
    for date in sere:
        split_time = date.split('T')
        year.append(split_time[0][0:4]) 
        month.append(split_time[0][4:6])
        day.append(split_time[0][6:8])
        caldate.append( (split_time[0][0:4] + '-' + split_time[0][4:6] + '-' +split_time[0][6:8]) )
        if len(split_time) < 2:
            time.append('NA')
        else:
            time.append((split_time[1][0:2] + ':' + split_time[1][2:4]) )
    # add lists as data columns
    data[('YEAR_' + name)] = year
    data[('MONTH_' + name)] = month
    data[('DAY_' + name)] = day
    data[('CALDATE_' + name)] = caldate
    data[('TIME_' + name)] = time
    return data

# execute time columns builder
dataset = dateSelector(dataset, dataset['DTSTART'], 'START')
dataset = dateSelector(dataset, dataset['DTEND'], 'END')

# copy dataset
data = dataset.copy()

# remove NAs
data = dataset[dataset['TIME_START'] != 'NA']

# transform time in datetime 
t1 =  pd.to_datetime(data['TIME_START'], format='%H:%S')
t2 =  pd.to_datetime(data['TIME_END'], format='%H:%S')

# subtract the local GMT
localGMT = pd.to_datetime('1900-01-01 03:00:00')
ta = t1 - localGMT
tb = t2 - localGMT 

# transform string and select time
strer = lambda x: str(x)
slicer = lambda x: x[len(x)-8:len(x)]

tx = ta.apply(strer)
tx = tx.apply(slicer)

ty = tb.apply(strer)
ty = ty.apply(slicer)

# transform in datetime
t01 =  pd.to_datetime(tx)
t02 =  pd.to_datetime(ty)

# SAVE TIME DURATION
time_duration = t02 - t01
time_duration = time_duration.apply(strer)
time_duration = time_duration.apply(slicer)
data['TIME_DURATION'] = pd.to_datetime(time_duration).dt.time

#===================#
# SAVE DATA
#===================#

data.to_csv('CALENDAR_DATA.csv')