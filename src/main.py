import json
from icalendar import Calendar, Event, Alarm
from datetime import date, datetime, timedelta

from icalendar.caselessdict import CaselessDict


class icalGen:
    def __init__(self, team, days, name):
        self.team = team
        self.days = days
        self.name = name
        self.numberOfNames = len(self.name)
        self.dstartArr = []

    def daysExt(self):
        pass

    def numberOfNames(self):
        self.numberOfNames = len(self.name)

    def dayConverter(self):
        weekdayConvert = []
        for dayStr in self.days:
            if dayStr.lower() == "mo" or dayStr.lower() == "mon":
                weekdayConvert.append(0)
            if dayStr.lower() == "di" or dayStr.lower() == "die":
                weekdayConvert.append(1)
            if dayStr.lower() == "mi" or dayStr.lower() == "mit":
                weekdayConvert.append(2)
            if dayStr.lower() == "do" or dayStr.lower() == "don":
                weekdayConvert.append(3)
            if dayStr.lower() == "fr" or dayStr.lower() == "fri":
                weekdayConvert.append(4)
            if dayStr.lower() == "sa" or dayStr.lower() == "sam":
                weekdayConvert.append(5)
            if dayStr.lower() == "so" or dayStr.lower() == "son":
                weekdayConvert.append(6)

        # Todo: in __init__
        start_date = datetime(2021, 1, 1)
        end_date = datetime(2022, 1, 1)
        delta = timedelta(days=1)
        calanderWeek = int(start_date.strftime("%U"))

        while start_date <= end_date:
            for dayInt in weekdayConvert:
                if (start_date.weekday() == dayInt):
                    # ics time format = "yyyyMMdd'T'HHmmss"
                    # print(start_date.strftime("%Y%m%d"+"T"+"%H%M%S"))
                   # print(start_date.strftime("%Y-%m-%d" + "-T" + "%H%M%S"))
                    self.dstartArr.append(
                        (start_date.strftime("%Y-%m-%d" + "-T" + "%H%M%S"))
                    )
            start_date += delta
                

    def writeIcal(self):
        self.dayConverter()

        calanderWeekArr = []
        weeksDividedByDays= {}
        weekCounter = 0
        for i in self.dstartArr:
            # CHANGE strptime
            calanderWeekArr.append(int((datetime.strptime(i,"%Y-%m-%d" + "-T" + "%H%M%S")).strftime("%V")))
        
        # Devide Days Into Weeks
        for i in range(0,len(calanderWeekArr)):
            if(calanderWeekArr[i] != calanderWeekArr[i-1]):
                weekCounter = i
                weeksDividedByDays[weekCounter] = []
            
            weeksDividedByDays[weekCounter].append(self.dstartArr[i])
  
        print(weeksDividedByDays.keys())


Bild = icalGen("Bild", ["MI", "Do"], ["Dominik", "Peter","Andreas"])
Bild.writeIcal()
