from icalendar import Calendar, Event, Alarm
from datetime import date, datetime, timedelta


class addICS:
    def __init__(self, file):
        self.file = file
        self.cal = Calendar()

        self.cal.add("version", "2.0")
        self.cal.add("prodid", "Technik-Kalender")

    def add(
        self, dateStart, dateEnd, summary, location="", description="", categories=""
    ):
        event = Event()
        alarm = Alarm()
        alarm.add("description","This is an event reminder")
        alarm.add("action","DISPLAY")
        alarm.add("trigger",timedelta(minutes=-10))
        event.add("summary", summary)
        event.add("location", location)
        event.add("categories", categories, encode=0)
        event.add("description", description)
        event.add("dtstart", dateStart)
        event.add("dtend", dateEnd)
        event.add("dtstamp", datetime.now())
        event.add("priority", 5)

        event.add_component(alarm)
        self.cal.add_component(event)

    def save(self):
        f = open(self.file, "wb")
        f.write(self.cal.to_ical())
        f.close()

