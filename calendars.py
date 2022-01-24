from bs4 import BeautifulSoup
from icalendar import Calendar, Event, TimezoneStandard, Alarm
from datetime import datetime, timedelta
import icalendar
import json
import random
from dateutil.rrule import rruleset
from datetime import datetime
from pytz import timezone

def open_and_bs4_file():
     files = open("KFUPM _ Course Offering.html", "r")
     soup = BeautifulSoup(files, "html.parser")

     schedule(soup)


def days(i):
     days_list = ["SU", "MO", "TU", "WE", "TH"]

     return days_list[i]


def schedule(soup):
     cal = create_file()
     term = soup.find(class_="term").text.replace("Term ", "")
     schedule = soup.find_all(class_="Hour")

     for i in schedule:
          i = str(i)

          day_index = int(i.split(";")[2].replace(" --day:", "")) - 1
          day = days(day_index)

          splitted = i.split(">")
          class_info = splitted[3].replace("</div", "").split("@")
          class_name = class_info[0]
          class_building = class_info[1]

          start_time = splitted[8].replace("</span", "")
          end_time = splitted[10].replace("</span", "")

          events(cal, class_name, class_building, start_time, end_time, day, term, day_index)

     f = open('example.ics', 'wb')
     f.write(cal.to_ical())
     f.close()


def create_file():
     cal = Calendar()
     cal.add('version', '2.0')
     cal.add('prodid', '-//www.kfupm.edu.sa//iCal Schedule Maker//EN')
     cal.add("calscale", "GREGORIAN")
     cal.add("x-wr-calname", "Academic Schedule 2021-2022 (1443H): Second Semester (212)")
     cal.add("x-wr-timezone","Asia/Riyadh")
     tz = vtimezone(cal)
     cal.add_component(tz)

     return cal



def vtimezone(cal):
     tz = icalendar.cal.Timezone()
     tz.add('TZID', "Asia/Riyadh")
     tz.add("tzurl", "http://tzurl.org/zoneinfo-outlook/Asia/Riyadh")
     tz.add('x-lic-location', "Asia/Riyadh")
     standard = TimezoneStandard(DTSTART="20100101T000000", TZOFFSETFROM="+0300", TZOFFSETTO="+0300", TZNAME="Eastern Province")
     tz.add_component(standard)

     return tz


def acad_file(term):
     f = open("acad.json")
     js = json.load(f)

     return js[term]


def events(cal, class_name, class_locatoin, start_time, end_time, day, term, day_index):
     file = acad_file(term)
     acad = file["acad"]
     start = str(int(acad["start"]) + day_index)
     end = acad["end"]
     exdates = tuple(acad["exclude"])

     class_no_sectoin = class_name.split("-")[0]
     class_building = class_locatoin.split("-")[0]
     class_room = class_locatoin.split("-")[1]

     event = Event()
     number = random.randint(100000000, 999999999)
     KSA = timezone('Asia/Riyadh')

     event.add('dtstamp', datetime(2022,1,1,0,0,0,tzinfo=KSA))
     event['uid'] = f'20220101T000000-{number}@kfupm.edu.sa'

     event.add('dtstart', datetime(int(start[0:4]),int(start[4:6]),int(start[6:8]),int(start_time[0:2]),int(start_time[2:4]),0,tzinfo=KSA))
     event.add('dtend', datetime(int(start[0:4]),int(start[4:6]),int(start[6:8]),int(end_time[0:2]),int(end_time[2:4]),0,tzinfo=KSA))

     event.add('summary', f'{class_name}')
     event.add('rrule', {'freq': 'WEEKLY', "BYDAY":f"{day}", "UNTIL":datetime(int(end[0:4]),int(end[4:6]),int(end[6:8]),int(end_time[0:2]),int(end_time[2:4]),0)})
     event.add('url', "https://registrar.kfupm.edu.sa/courses-classes/course-offering/?old")
     event.add("DESCRIPTION", f"You have a {class_no_sectoin} class at building {class_building} in room {class_room}.")
     event.add("LOCATION", f"Building {class_locatoin}")
     event.add("TRANSP", "OPAQUE")
     event.add("X-MICROSOFT-CDO-BUSYSTATUS", "BUSY")
     event = alarm(event, class_no_sectoin, class_building, class_room)
     event = get_exdate(event, exdates, start_time)

     cal.add_component(event)

     return cal


def alarm(event, class_no_sectoin, class_building, class_room):
     alarm = Alarm()
     alart_time = timedelta(minutes=-int(15))
     alarm.add("trigger", alart_time)
     alarm.add("action", "display")
     alarm.add("DESCRIPTION", f"You have a {class_no_sectoin} class at building {class_building} in room {class_room}.")
     event.add_component(alarm)

     return event


def get_exdate(event, exdates, start_time):
     rules = rruleset()

     dates = []
     for i in exdates:
          date = datetime(int(i[0:4]), int(i[4:6]), int(i[6:8]), int(start_time[0:2]),int(start_time[2:4]),0)
          event.add("exdate",date)

     return event



def main():
     open_and_bs4_file()
     f_readable = open("example.ics", "r").read()
     txt = f_readable.replace("EXDATE:", "EXDATE;TZID=Asia/Riyadh:")

     f = open('example.ics', 'w')
     f.write(txt)
     f.close()
main()