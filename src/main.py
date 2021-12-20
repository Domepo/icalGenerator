import json
from icalendar import Calendar, Event, Alarm
from datetime import date, datetime, timedelta
from icalendar.caselessdict import CaselessDict


class iCalendar:
    def __init__(self, file):
        self.file = file
        self.cal = Calendar()

        self.cal.add("version", "2.0")
        self.cal.add("prodid", "Dome und Leon Parser")

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
                if start_date.weekday() == dayInt:
                    # ics time format = "yyyyMMdd'T'HHmmss"
                    # print(start_date.strftime("%Y%m%d"+"T"+"%H%M%S"))
                    # print(start_date.strftime("%Y-%m-%d" + "-T" + "%H%M%S"))
                    self.dstartArr.append(
                        (start_date.strftime("%Y-%m-%d" + "-T" + "%H%M%S"))
                    )
            start_date += delta

    def weekDivider(self):
        self.dayConverter()

        calanderWeekArr = []
        weeksDividedByDays = {}
        weekCounter = 0
        for i in self.dstartArr:
            # CHANGE strptime
            calanderWeekArr.append(
                int((datetime.strptime(i, "%Y-%m-%d" + "-T" + "%H%M%S")).strftime("%V"))
            )

        # Divide Days Into Weeks
        weekCounter = 1
        for i in range(0, len(calanderWeekArr)):
            if calanderWeekArr[i] != calanderWeekArr[i - 1]:
                weeksDividedByDays[weekCounter] = []
                weekCounter += 1
            weeksDividedByDays[weekCounter - 1].append(self.dstartArr[i])
        return weeksDividedByDays

    def formatIcal(self):
        # Assign names to weeks/appointment
        weeksDividedByNames = {}
        weeksDividedByNamesFormat = {}
        weeksDividedByDays = self.weekDivider()
        for k, p in enumerate(self.name):
            weeksDividedByNames[p] = []
            for i in weeksDividedByDays:
                if i % self.numberOfNames == k:
                    weeksDividedByNames[p].append(weeksDividedByDays[i])

            weeksDividedByNamesFormat[p] = []
            for i in weeksDividedByNames.get(p):
                for l in i:
                    weeksDividedByNamesFormat[p].append(l)

        return weeksDividedByNamesFormat

    def hoursDelta(self, hoursV):
        return timedelta(hours=hoursV)

    def writeIcal(self):
        formatIcal = self.formatIcal()

        # print(formatIcal)
        a = iCalendar("/Users/dominik/Desktop/Github/icalGenerator/src/a.ics")
        for i in formatIcal:
            # print(i)
            for c in formatIcal[i]:
                # print(c)
                daytime = datetime.strptime(c, "%Y-%m-%d" + "-T" + "%H%M%S")
                #
                # Todo:
                # get value from {"MI":10, "Do":10,"So":10}
                #
                if daytime.weekday() == 2:
                    startDate = daytime + self.hoursDelta(18)
                elif daytime.weekday() == 4:
                    startDate = daytime + self.hoursDelta(19)
                elif daytime.weekday() == 6:
                    startDate = daytime + self.hoursDelta(10)
                else:
                    startDate = daytime + self.hoursDelta(10)

                endDate = startDate + self.hoursDelta(1)
                #
                #
                #

                a.add(startDate, endDate, i + " " + self.team, "EFG", i, "Tontechnik")
        a.save()


Bild = icalGen("Bild", {"MI": 10, "Do": 10, "So": 10}, ["Dominik", "Peter", "Andreas"])
Bild.writeIcal()
