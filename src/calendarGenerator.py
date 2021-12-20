from datetime import date, datetime, timedelta
from functools import WRAPPER_ASSIGNMENTS

class ics:
    def __init__(self, team="", nameAndDay={}):
        self.team = team
        self.nameAndDay = nameAndDay
        self.names = []
        self.numberOfNames = len(self.nameAndDay)
        self.sortWeekdaysToNamesDict = {}
        self.allDatesWithIndex = []
        self.startDate = datetime(2021, 1, 1)
        self.endDate = datetime(2022, 1, 1)
        self.delta = timedelta(days=1)

    def sortWeekdaysToNames(self):
        # 0 = Monday
        # 1 = Thurstday ....
        for index, names in enumerate(self.nameAndDay):
            #print(index, names, self.nameAndDay[names])
            self.names.append(names)
            for name in self.nameAndDay[names]:
                try:
                    self.sortWeekdaysToNamesDict[name].append(names)
                except:
                    self.sortWeekdaysToNamesDict[name] = []    
                    self.sortWeekdaysToNamesDict[name].append(names)
        #print(self.sortWeekdaysToNamesDict)
        return(self.sortWeekdaysToNamesDict)

    def convertDayIndexToDate(self):
        # Todo: in __init__
        #
        # converts 0,1 -> 2021.01.04(Monday), 2021,01,05(Thursday)
        #
        while self.startDate <= self.endDate:
            for dayInt in self.sortWeekdaysToNamesDict.keys():
                if self.startDate.weekday() == dayInt:
                    # ics time format = "yyyyMMdd'T'HHmmss"
                    self.allDatesWithIndex.append(
                        (self.startDate.strftime("%Y-%m-%d" + "-T" + "%H%M%S"),self.sortWeekdaysToNamesDict[dayInt])
                    )
            self.startDate += self.delta

        sortNamesToWeekdays = []
        sortNamesToWeekdaysCounter = 0
        for d in (self.allDatesWithIndex):
            sortNamesToWeekdays.append([d[1]])
            sortNamesToWeekdays[sortNamesToWeekdaysCounter].append(d[0])
            sortNamesToWeekdaysCounter+=1
        sortNamesToWeekdays.sort()
        
        combineDatesToNames = []
        combineDatesToNamesCounter = 0
        for ix,dc in enumerate(sortNamesToWeekdays):
            #print(sortNamesToWeekdays[ix][0])
            # Maybe buggy
            # len(sortNamesToWeekdays)-1 can limit the loop
            if(ix < len(sortNamesToWeekdays)-1):
                if(sortNamesToWeekdays[ix][0] == sortNamesToWeekdays[ix+1][0] ):
                    if(sortNamesToWeekdays[ix][0] not in combineDatesToNames):
                        combineDatesToNames.append(sortNamesToWeekdays[ix][0]) 
                    else:
                        combineDatesToNames[combineDatesToNamesCounter].append(sortNamesToWeekdays[ix][1])

                else:
                    combineDatesToNamesCounter+=1


                

        print(combineDatesToNames)
        return(self.allDatesWithIndex)


a = ics("Video", {"Dominik": [0, 1], "Andreas": [1, 2], "Peter": [1, 2]})
a.sortWeekdaysToNames()
a.convertDayIndexToDate()
# a.weekDivider()
# a.formatIcal()
