from bs4 import BeautifulSoup
import icalendar
from datetime import datetime, timedelta
import json
import random
from pytz import timezone


def open_file_get_soup():
     files = open("KFUPM _ Course Offering.html", "r")
     soup = BeautifulSoup(files, "html.parser")

     schedule(soup)


def days(i):
     days_list = ["SU", "MO", "TU", "WE", "TH"]

     return days_list[i]


def schedule(soup):
     cal = create_cal()

     term = soup.find(class_="term").text.replace("Term ", "")
     schedule = soup.find_all(class_="Hour")

     for i in schedule:
          i = str(i)

          day_index = int(i.split(";")[2].replace(" --day:", "")) - 1
          day_name = days(day_index)

          splitted = i.split(">")
          class_info = splitted[3].replace("</div", "").split("@")
          class_name = class_info[0]
          class_building = class_info[1]

          start_time = splitted[8].replace("</span", "")
          end_time = splitted[10].replace("</span", "")

          events(cal, class_name, class_building, start_time, end_time, day_name, term, day_index)

     f = open("example.ics", "wb")
     f.write(cal.to_ical())
     f.close()


def create_cal():
     cal = icalendar.cal.Calendar()

     cal.add("VERSION", "2.0")
     cal.add("PRODID", "-//www.kfupm.edu.sa//iCal Schedule Maker//EN")
     cal.add("CALSCALE", "GREGORIAN")
     cal.add("X-WR-CALNAME", "Academic Schedule 2021-2022 (1443H): Second Semester (212)")
     cal.add("X-WR-TIMEZONE","Asia/Riyadh")

     vtimezone(cal)

     return cal


def vtimezone(cal):
     tz = icalendar.cal.Timezone()

     tz.add("TZID", "Asia/Riyadh")
     tz.add("TZURL", "http://tzurl.org/zoneinfo-outlook/Asia/Riyadh")
     tz.add("X-LIC-LOCATION", "Asia/Riyadh")

     standard(tz)

     cal.add_component(tz)

     return cal


def standard(tz):
     standard_timezone = icalendar.cal.TimezoneStandard()
     standard_timezone.add("DTSTART", datetime(2010,1,1,0,0,0))
     standard_timezone.add("TZOFFSETFROM", timedelta(hours=+int(3)))
     standard_timezone.add("TZOFFSETTO", timedelta(hours=+int(3)))
     standard_timezone.add("TZNAME", "Eastern Province")

     tz.add_component(standard_timezone)

     return tz


def load_file_get_term(term):
     f = open("acad.json")
     json_file = json.load(f)

     return json_file[term]


def events(cal, class_name, class_locatoin, start_time, end_time, day_name, term, day_index):
     load_term = load_file_get_term(term)
     acad = load_term["acad"] ##############################################################################################
     start = str(int(acad["start"]) + day_index) ###########################################################################
     end = acad["end"]
     exdates = acad["exclude"]

     class_no_sectoin = class_name.split("-")[0]
     class_building = class_locatoin.split("-")[0]
     class_room = class_locatoin.split("-")[1]


     event = icalendar.cal.Event()
     KSA = timezone("Asia/Riyadh")
     event.add("DTSTAMP", datetime(2022,1,1,0,0,0,tzinfo=KSA))

     number = random.randint(100000000, 999999999)
     event.add("UID", f"20220101T000000-{number}@kfupm.edu.sa")
     event.add("DTSTART", datetime(int(start[0:4]),int(start[4:6]),int(start[6:8]),int(start_time[0:2]),int(start_time[2:4]),0,tzinfo=KSA))
     event.add("DTEND", datetime(int(start[0:4]),int(start[4:6]),int(start[6:8]),int(end_time[0:2]),int(end_time[2:4]),0,tzinfo=KSA))
     event.add("SUMMARY", class_name)
     event.add("RRULE", {"freq": "WEEKLY", "BYDAY":day_name, "UNTIL":datetime(int(end[0:4]),int(end[4:6]),int(end[6:8]),int(end_time[0:2]),int(end_time[2:4]),0)})
     event.add("URL", "https://registrar.kfupm.edu.sa/courses-classes/course-offering/?old")
     event.add("DESCRIPTION", f"You have a {class_no_sectoin} class at building {class_building} in room {class_room}.")
     event.add("LOCATION", f"Building {class_locatoin}")
     event.add("TRANSP", "OPAQUE")
     event.add("X-MICROSOFT-CDO-BUSYSTATUS", "BUSY")
     alarm(event, class_no_sectoin, class_building, class_room)
     get_exdate(event, exdates, start_time)

     cal.add_component(event)

     return cal


def alarm(event, class_no_sectoin, class_building, class_room):
     alarm = icalendar.cal.Alarm()
     alarm.add("TRIGGER", timedelta(minutes=-int(10)))
     alarm.add("ACTION", "DISPLAY")
     alarm.add("DESCRIPTION", f"You have a {class_no_sectoin} class at building {class_building} in room {class_room}.")
     event.add_component(alarm)

     return event


def get_exdate(event, exdates, start_time):
     for i in exdates:
          date = datetime(int(i[0:4]), int(i[4:6]), int(i[6:8]), int(start_time[0:2]),int(start_time[2:4]),0)
          event.add("exdate",date)

     return event


def add_tzid():
     f_readable = open("example.ics", "r").read()
     txt = f_readable.replace("EXDATE:", "EXDATE;TZID=Asia/Riyadh:")

     f = open("example.ics", "w")
     f.write(txt)
     f.close()

def main():
     open_file_get_soup()
     add_tzid()
main()