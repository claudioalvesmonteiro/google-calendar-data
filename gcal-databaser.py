'''
TEXT MINING OF ICS FILE FROM GOOGLE CALENDAR

Takes the ics file as input and 
export a CSV dataset with the informations
'''

# import modules
import pandas as pd

'''

 search for the keywords and append to var dictionary of list

'''

file = 'claudiomonteirol.a@gmail.com.ics'

def listToData(file):

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

# remove BEFORE:

# split DSTART e DTEND in date,time columns each