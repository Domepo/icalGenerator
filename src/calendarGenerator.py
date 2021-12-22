from datetime import date, datetime, timedelta
from icalendar import Calendar, Event, Alarm

class iCalendar:
    def __init__(self, file):
        self.file = file
        self.cal = Calendar()

        self.cal.add("version", "2.0")
        self.cal.add("prodid", "Technik-Kalender")

    def add(
        self, dateStart, dateEnd, summary, location="", description="", categories=""
    ):
        event = Event()

        event.add("summary", summary)
        event.add("location", location)
        event.add("categories", categories, encode=0)
        event.add("description", description)
        event.add("dtstart", dateStart)
        event.add("dtend", dateEnd)
        event.add("dtstamp", datetime.now())
        event.add("priority", 5)

        self.cal.add_component(event)

    def save(self):
        f = open(self.file, "wb")
        f.write(self.cal.to_ical())
        f.close()


class ics:
    def __init__(self, team="", nameAndDay={},timesForAppointments={}):
        self.team = team
        self.nameAndDay = nameAndDay
        self.timesForAppointments = timesForAppointments
        self.names = []
        self.numberOfNames = len(self.nameAndDay)
        self.sortWeekdaysToNamesDict = {}
        self.allDatesWithIndex = []
        self.startDate = datetime(2022, 1, 1)
        self.endDate = datetime(2023, 1, 1)
        self.delta = timedelta(days=1)

    def sortWeekdaysToNames(self):
        # 0 = Monday
        # 1 = Thurstday ....
        for index, names in enumerate(self.nameAndDay):
            # print(index, names, self.nameAndDay[names])
            self.names.append(names)
            for name in self.nameAndDay[names]:
                try:
                    self.sortWeekdaysToNamesDict[name].append(names)
                except:
                    self.sortWeekdaysToNamesDict[name] = []
                    self.sortWeekdaysToNamesDict[name].append(names)
        # print(self.sortWeekdaysToNamesDict)
        return self.sortWeekdaysToNamesDict

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
                        (
                            self.startDate.strftime("%Y-%m-%d" + "-T" + "%H%M%S"),
                            self.sortWeekdaysToNamesDict[dayInt],
                        )
                    )
            self.startDate += self.delta

        sortNamesToWeekdays = []
        sortNamesToWeekdaysCounter = 0
        for d in self.allDatesWithIndex:
            sortNamesToWeekdays.append([d[1]])
            sortNamesToWeekdays[sortNamesToWeekdaysCounter].append(d[0])
            sortNamesToWeekdaysCounter += 1
        sortNamesToWeekdays.sort()

        combineDatesToNames = {}
        for ix in range(0,len(sortNamesToWeekdays)):
            try:
                def addDateAndCalenderDay():
                    combineDatesToNames[tuple(sortNamesToWeekdays[ix][0])].append(
                        [
                            # {"['Dominik', 'Andreas']": [['2021-01-06-T000000', '01']
                            sortNamesToWeekdays[ix][1],
                            (
                                datetime.strptime(
                                    sortNamesToWeekdays[ix][1],
                                    "%Y-%m-%d" + "-T" + "%H%M%S",
                                )
                            ).strftime("%V"),
                        ]
                    )
                addDateAndCalenderDay()
            except:
                combineDatesToNames[tuple(sortNamesToWeekdays[ix][0])] = []
                addDateAndCalenderDay ()
        #print(combineDatesToNames)
        return combineDatesToNames

    def sortNamesToEachDate(self):
        sortedDateCalenderWeekNameList = []
        checkEvenOdd = 0
        splitEvenDaysToNamesCounter = 0
        splitOddDaysToNamesCounter = 0
        #print(self.convertDayIndexToDate())
        for namesOfList in self.convertDayIndexToDate():            
            combinedDatesToNames = self.convertDayIndexToDate()[namesOfList]
            # check for dates in same Week
            for i, j in enumerate(combinedDatesToNames[:-1]):
                # One Person should do one week
                if j[1]  == combinedDatesToNames[i+1][1]: 
                    for dateIndex, eachDate in enumerate(combinedDatesToNames):
                        if splitEvenDaysToNamesCounter < len(namesOfList) - 1:
                            splitEvenDaysToNamesCounter += 1
                        else:
                            splitEvenDaysToNamesCounter = 0
                        combinedDatesToNames[i+1].insert(2,namesOfList[splitEvenDaysToNamesCounter])
                        combinedDatesToNames[i].insert(2,namesOfList[splitEvenDaysToNamesCounter])
                        break 

            # check for dates in different Week
            for i in range(0,len(combinedDatesToNames)):
                    try:
                        if(type(combinedDatesToNames[i][2]) == str):
                            checkEvenOdd = 0
                            pass
                    except:
                        checkEvenOdd = 1
                        pass
                    if(checkEvenOdd == 1):
                        if splitOddDaysToNamesCounter < len(namesOfList)-1:
                            splitOddDaysToNamesCounter += 1
                        else:
                            splitOddDaysToNamesCounter = 0
                        combinedDatesToNames[i].insert(2,namesOfList[splitOddDaysToNamesCounter])
            # put all weeks/people in obe arraay
            for i in combinedDatesToNames:
                sortedDateCalenderWeekNameList.append(i)
        return sortedDateCalenderWeekNameList

        #print(sortedDateCalenderWeekNameList)
    def writeICS(self):
        a = iCalendar("/Users/dominik/Desktop/Github/icalGenerator/src/a.ics")
        #timesForAppointments
        for i in self.sortNamesToEachDate():
            #print(i[0])
            day = datetime.strptime(i[0], "%Y-%m-%d" + "-T" + "%H%M%S")
            # set times for appointments
            for weekDay in self.timesForAppointments:
                if(day.weekday() == weekDay):
                    splittedTime =self.timesForAppointments[weekDay].split(":")
                    for hoursMinutes in splittedTime:
                        hours,minutes = int(splittedTime[0]),int(splittedTime[1])
                        staratTime = timedelta(hours=hours, minutes=minutes)
                        endTime = timedelta(hours=hours+1, minutes=minutes)

            a.add(day+staratTime, day+endTime, i[2]+" macht heute "+self.team, "EFG", i[2], self.team)
        a.save()

# Mo = 0
# Di = 1
# Mi = 2
# Do = 3
# Fr = 4
# Sa = 5
# So = 6
a = ics("Bildtechnik", {"Gerd": [2,4,6], "Josef": [6],"Frank":[2,4,6]},{2:"18:30",4:"19:00",5:"20:00",6:"10:00"})
a.writeICS()

