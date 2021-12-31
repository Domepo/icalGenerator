# icalGenerator Is A Tool To Convert Team-Appiontments To An ICS File

# ┌────────────────────────────┐            ┌──────────────────────────────────────────────────────────────────────┐
# │           Input            │      ┌─────▶                             Output                                   │
# │┌──────────────────────────┐│      │     │                                                                      │
# ││  Peter: Monday, Sunday   ││      │     │┌─Monday─┐┌─Tuesday┐┌Wednesday┌Thursday┐┌─Friday─┐┌Saturday┐┌─Sunday─┐│
# │└──────────────────────────┘│      │     ││        ││        ││        ││        ││        ││        ││        ││
# │┌──────────────────────────┐│──────┘     ││Peter   ││        ││        ││        ││        ││Ken     ││Peter   ││
# ││  Ken: Saturday, Monday   ││            ││        ││        ││        ││        ││        ││        ││        ││
# │└──────────────────────────┘│            │└1───────┘└2───────┘└3───────┘└4───────┘└5───────┘└6───────┘└7───────┘│
# │┌──────────────────────────┐│            │┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐│
# ││  Ben:           Monday   ││            ││        ││        ││        ││        ││        ││        ││        ││
# │└──────────────────────────┘│            ││Ken     ││        ││        ││        ││        ││Ken     ││Peter   ││
# └────────────────────────────┘            ││        ││        ││        ││        ││        ││        ││        ││
#                                           │└8───────┘└9───────┘└10──────┘└11──────┘└12──────┘└13──────┘└14──────┘│
#                                           │┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐│
#                                           ││        ││        ││        ││        ││        ││        ││        ││
#                                           ││Ben     ││        ││        ││        ││        ││Ken     ││Peter   ││
#                                           ││        ││        ││        ││        ││        ││        ││        ││
#                                           │└15──────┘└16──────┘└17──────┘└18──────┘└19──────┘└20──────┘└21──────┘│
#                                           │┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐│
#                                           ││        ││        ││        ││        ││        ││        ││        ││
#                                           ││Peter   ││        ││        ││        ││        ││Ken     ││Peter   ││
#                                           ││        ││        ││        ││        ││        ││        ││        ││
#                                           │└22──────┘└23──────┘└24──────┘└25──────┘└26──────┘27───────┘└28──────┘│
#                                           │┌────────┐┌────────┐┌────────┐                                        │
#                                           ││        ││        ││        │                                        │
#                                           ││Ken     ││        ││        │                                        │
#                                           ││        ││        ││        │                                        │
#                                           │└29──────┘30───────┘└31──────┘                                        │
#                                           └──────────────────────────────────────────────────────────────────────┘

from datetime import date, datetime, timedelta
from addCalendar import addICS


class icsGenerator:
    def __init__(
        self,
        team="",
        nameAndDay={},
        timesForAppointments={},
        tagTeam=bool,
        tagTeamDay=int,
        startDate=type(datetime),
        endDate=type(datetime),
    ):
        self.team = team
        self.nameAndDay = nameAndDay
        self.timesForAppointments = timesForAppointments
        self.tagTeam = tagTeam
        self.tagTeamDay = tagTeamDay
        self.startDate = startDate
        self.endDate = endDate
        # Stored names
        self.names = []
        self.numberOfNames = len(self.nameAndDay)
        self.sortWeekdaysToNamesDict = {}
        self.allDatesWithIndex = []
        # Time between each day (usefull to skip every odd day e.g)
        self.delta = timedelta(days = 1)
        self.h = 0

    def sortWeekdaysToNames(self):
        # ***Input (self.nameAndDay)
        # {'Peter': [0,6], 'Ken': [5,0], 'Ben': [0]}
        for index, names in enumerate(self.nameAndDay):
            self.names.append(names)
            for name in self.nameAndDay[names]:
                try:
                    self.sortWeekdaysToNamesDict[name].append(names)
                except:
                    self.sortWeekdaysToNamesDict[name] = []
                    self.sortWeekdaysToNamesDict[name].append(names)
        # ***Output (self.sortWeekdaysToNamesDict)
        # {0: ["Peter","Ken","Ben"],5:["Ken"],6:["Ben"]}
        return self.sortWeekdaysToNamesDict

    def convertDayIndexToDatetimeWithNames(self):
        # ***Input (self.sortWeekdaysToNamesDict.keys())
        # [0,5,6]
        # ***Output
        # 2021.01.04(Monday), 2021.01.09(Saturday), 2021.01.10(Sunday)
        # ↓
        # ('2022-01-01-T000000', ['Ken']), 
        # ('2022-01-02-T000000', ['Peter']), 
        # ('2022-01-03-T000000', ['Peter', 'Ken', 'Ben']),

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
        # print(self.allDatesWithIndex)
    def convertDayIndexToWeekday(self):
        # ***Input
        # [0,5,6]
        # ***Output
        # ['2022-01-01-T000000', '01'], 
        # ['2022-01-02-T000000', '01'], 
        # ['2022-01-03-T000000', '01'],
        # ['2022-01-08-T000000', '02'], 
        sortNamesToWeekdays = []
        sortNamesToWeekdaysCounter = 0
        for d in self.allDatesWithIndex:
            sortNamesToWeekdays.append([d[1]])
            sortNamesToWeekdays[sortNamesToWeekdaysCounter].append(d[0])
            sortNamesToWeekdaysCounter += 1
        sortNamesToWeekdays.sort()

        combineDatesToNames = {}
        for ix in range(0, len(sortNamesToWeekdays)):
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
                addDateAndCalenderDay()
        # print(combineDatesToNames)
        self.a = combineDatesToNames
        #print(combineDatesToNames)
        return combineDatesToNames


    def sortNamesToEachDate(self):
        sortedDateCalenderWeekNameList = []
        checkEvenOdd = 0
        splitEvenDaysToNamesCounter = 0
        splitOddDaysToNamesCounter = 0
        #print(self.convertDayIndexToWeekday())
        for namesOfList in self.convertDayIndexToWeekday():
            combinedDatesToNames = self.convertDayIndexToWeekday()[namesOfList]
            # check for dates in same Week
            for i, j in enumerate(combinedDatesToNames[:-1]):
                # One Person should do one week
                if j[1] == combinedDatesToNames[i + 1][1]:
                    for dateIndex, eachDate in enumerate(combinedDatesToNames):
                        if splitEvenDaysToNamesCounter < len(namesOfList) - 1:
                            splitEvenDaysToNamesCounter += 1
                        else:
                            splitEvenDaysToNamesCounter = 0
                        combinedDatesToNames[i + 1].insert(
                            2, namesOfList[splitEvenDaysToNamesCounter]
                        )
                        combinedDatesToNames[i].insert(
                            2, namesOfList[splitEvenDaysToNamesCounter]
                        )
                        break

            # check for dates in different Week
            for i in range(0, len(combinedDatesToNames)):
                try:
                    if type(combinedDatesToNames[i][2]) == str:
                        checkEvenOdd = 0
                        pass
                except:
                    checkEvenOdd = 1
                    pass
                if checkEvenOdd == 1:
                    if splitOddDaysToNamesCounter < len(namesOfList) - 1:
                        splitOddDaysToNamesCounter += 1
                    else:
                        splitOddDaysToNamesCounter = 0
                    combinedDatesToNames[i].insert(
                        2, namesOfList[splitOddDaysToNamesCounter]
                    )
            # put all weeks/people in obe arraay
            for i in combinedDatesToNames:
                sortedDateCalenderWeekNameList.append(i)
        return sortedDateCalenderWeekNameList

        # print(sortedDateCalenderWeekNameList)

    def getNamesOnSpecificDate(self):
        def rotate(l, n):
            return l[n:] + l[:n]

        uuu = []
        for i in self.sortNamesToEachDate():
            # print(i)
            if (
                datetime.strptime(i[0], "%Y-%m-%d" + "-T" + "%H%M%S").weekday()
                == self.tagTeamDay
            ):
                daay = datetime.strptime(i[0], "%Y-%m-%d" + "-T" + "%H%M%S")
                uuu.append(i[2])
        return rotate(uuu, self.tagTeamDay + 1)

    def countWeekDays(self):
        # print(self.nameAndDay.get("Dennis"))
        c = []
        for i in self.nameAndDay:
            o = self.nameAndDay.get(i)
            for k in o:
                c.append(k)
        # print(sorted(c))
        sameWeekdays = {}
        for i in set(c):
            sameWeekdays[i] = c.count(i)

        return sameWeekdays

    def writeICS(self):
        a = addICS(
            "/Users/dominik/Desktop/Github/icalGenerator/examples/"
            + str(self.team)
            + ".ics"
        )
        # timesForAppointments
        uuu = []
        ii = iter(self.getNamesOnSpecificDate())
        for e, i in enumerate(self.sortNamesToEachDate()):

            # print(i[0])
            day = datetime.strptime(i[0], "%Y-%m-%d" + "-T" + "%H%M%S")
            # set times for appointments
            for weekDay in self.timesForAppointments:
                if day.weekday() == weekDay:
                    splittedTime = self.timesForAppointments[weekDay].split(":")
                    for hoursMinutes in splittedTime:
                        hours, minutes = int(splittedTime[0]), int(splittedTime[1])
                        staratTime = timedelta(hours=hours, minutes=minutes)
                        endTime = timedelta(hours=hours + 1, minutes=minutes)

            a.add(
                day + staratTime,
                day + endTime,
                i[2] + " macht heute " + self.team,
                "EFG",
                i[2],
                self.team,
            )
            if (
                self.tagTeam == True
                and datetime.strptime(i[0], "%Y-%m-%d" + "-T" + "%H%M%S").weekday()
                == self.tagTeamDay
            ):
                z = next(ii)
                a.add(
                    day + staratTime,
                    day + endTime,
                    z + " Zweittechniker " + self.team,
                    "EFG",
                    z,
                    self.team,
                )
        a.save()
        # print(self.getNamesOnSpecificDate(),"a")


# Mo = 0
# Di = 1
# Mi = 2
# Do = 3
# Fr = 4
# Sa = 5
# So = 6
a = icsGenerator(
    "Lichttechnik",
    {
        "Peter": [0, 6],
        "Ken": [5, 0], 
        "Ben": [0]
    },
    {2: "18:30", 4: "19:00", 5: "20:00", 6: "10:00"},
    True,
    6,
    datetime(2022, 1, 1),
    datetime(2023, 1, 1),
)
a.sortWeekdaysToNames()
a.convertDayIndexToDatetimeWithNames()
# a.convertDayIndexToWeekday()
a.sortNamesToEachDate()
a.writeICS()
a.countWeekDays()
a.getNamesOnSpecificDate()
print(datetime.now().strftime("%Y%m%d" + "T" + "%H%M%S"))
print(type(datetime(2022, 1, 1)))
