'''
TEXT MINING OF ICS FILE FROM GOOGLE CALENDAR
'''


'''
Takes the ics file as input and 
export a CSV dataset with the informations
'''
#def icsTableGenerator():



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
    for event in cal:
        for info in event:
            for key, value in data.items():
                if key == 'SUMMARY':
                    if 'Alarm' not in info:
                        if key in info:
                            data[key].append(info)
                else:
                    if key in info:
                        data[key].append(info)
    return data


data = listToData(cal)

for key, value in data.items():
    print(key, len(value))

count = 0
for i in data['SUMMARY']:
    if 'Alarm' not in i:
        count += 1

count