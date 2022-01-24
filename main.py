import sys
import requests
from bs4 import BeautifulSoup
import json

dictionary = {}

def get_arguments():
     if (len(sys.argv) != 1):
          argv_list = []
          argvs = sys.argv[1::]

          for argv in argvs:
               argv_list.append(argv)

          argvs.sort(reverse=True)
     else:
          argv_list = None

     return argv_list


def get_current():
     url = ("https://registrar.kfupm.edu.sa/academic-calendar/current-academic-year/")

     return url


def get_future():
     url = ("https://registrar.kfupm.edu.sa/academic-calendar/future-academic-years/")

     return url


def get_past():
     url = ("https://registrar.kfupm.edu.sa/academic-calendar/past-academic-years/")

     return url


def get_term():
     years = get_arguments()

     current = get_current()
     future = get_future()
     past = get_past()

     for i in (current, future, past):
          html = (requests.get(i)).text
          soup = BeautifulSoup(html, 'html.parser')

          acap_options = soup.find(id="academic_calendar_option")
          prep_options = soup.find(id="academic_calendar_prep_year_option")

          for j in (0,1):
               if (j == 0):
                    url = ["academic-calendar"]
               else:
                    url = ["academic-prep-calendar-first-half", "academic-prep-calendar-second-half"]

               options = j.find_all('option')[1::]

               if (len(options) == 0):
                    continue

               for option in options:
                    value = option["value"]

                    if (years == None):
                         get_api(url, value)
                    else:
                         for year in years:
                              if (value[0:4] == year):
                                   get_api(url, value)

          continue

          for payload in payloads:
               html = (requests.post(url, data=payload)).content
               soup = BeautifulSoup(html, 'html.parser')
               options = soup.find_all('option')[1::]

               for option in options:
                    value = option["value"]

                    if (years == None):
                         get_tables(url, payload, value)
                    else:
                         for year in years:
                              if (value[0:4] == year):
                                   get_tables(url, payload, value)


def get_api(url, value):
     url = (f"https://registrar.kfupm.edu.sa/api/{url}?term_code={value}")
     response = requests.get(url.json)
     print(response)


def get_tables(url, payload, value):
     term = value[2:5]

     keys = " ".join(list(dictionary.keys()))

     if (keys.find(term) != -1):
          dictionary[term]["PREP"] = {"FIRST":{},"SECOND":{}}
     else:
          dictionary[term] = {}
          dictionary[term]["ACAD"] = {}

     last_key = list(payload.keys())[-1]
     payload[last_key] = value

     html = (requests.post(url, data=payload)).content
     soup = BeautifulSoup(html, 'html.parser')
     tables = soup.find_all(class_ = "table")

     get_dates_events(term, tables)


def get_dates_events(term, tables):
     first_line = False

     START = []
     END = []
     EXCLUDE = []
     NORMAL = []

     if (len(tables) == 1):
          academic = "ACAD"
     elif (len(tables) == 2):
          academic = "PREP"

     for table in tables:
          soup = BeautifulSoup(str(table), 'html.parser')

          path = dictionary[term][academic]

          if ((academic == "PREP")):
               table_index = tables.index(table)
               half = get_half(table_index)
               path = path[half]

          columns = soup.find_all("tr")[1::]

          for column in columns:
               rows = column.find_all('td')

               if (len(rows) == 4):
                    row = 2
               elif (len(rows) == 5):
                    row = 3

               date = (" ".join((rows[row].text).split())).lower()
               date = replacement(date)

               event = (" ".join((rows[row + 1].text).split())).lower()

               if (first_line == False):
                    years = get_years(date)
                    year = years[0]
                    next_year = years[1]

                    first_line = True
               elif (date[-2:].find(next_year[-2:]) != -1):
                    year = next_year

               if ((date.find("DEC") != -1) and (date.find("JAN") != -1)):
                    date = two_years(date, year)
               elif (date.find(year) != -1):
                    date = one_year(date, year)
               else:
                    date = not_one_year_nor_two_years(date, year)

               if (len(date) == 10):
                    date = "0" + date

               check_event(date, event, START, EXCLUDE, END, NORMAL)
          path["START"] = START
          path["END"] = END
          path["EXCLUDE"] = EXCLUDE
          path["NORMAL"] = NORMAL

          START = []
          EXCLUDE = []
          END = []
          NORMAL = []


def get_half(table_index):
     halfs = ["FIRST", "SECOND"]
     half = halfs[table_index]

     return half


def replacement(date):
     replace_from = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "."]
     replace_to = ["JAN", "FAB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

     for i in range(39):
          date = date.replace(replace_from[i], replace_to[i])

     return date


def get_years(date):
     year = date[-4:]
     next_year = str(int(year) + 1)

     return year, next_year


def two_years(date, year):
     dates = []

     date_spliited = (" ".join(date.replace("-", " - ").split())).split(" - ")

     for i in date_spliited:
          if (len(i) == 10):
               i = "0" + i

          splitted = i.split("'")

          if (len(splitted) == 1):
               dates.append(splitted[0])

               if (len(dates) == 1):
                    previous_year = str(int(year) - 1)
                    dates[0] = dates[0] + " " + previous_year
          else:
               dates.append(splitted[0] + " 20" + splitted[1])

     date = " - ".join(dates)

     return date


def one_year(date, year):
     dates = []

     date = " ".join(date.replace("%s" %year, "").split())

     if (date[-1].find("-") != -1):
          date = date.replace("-", " ")
     elif (len(date) == 5 or len(date) == 6):
          date = date.replace("-", " ")

     date_spliited = " ".join(date.replace("-", " - ").split()).split(" - ")

     if (len(date_spliited) != 1):
          for i in date_spliited:
               if ((len(i) == 1) or len(i) == 5):
                    i = "0" + i
               dates.append(i)

          date = " - ".join(dates)
     date = " ".join(date.split()) + " " + year

     return date


def not_one_year_nor_two_years(date, year):
     dates = []

     date_spliited = " ".join(date.replace("-", " - ").split()).split(" - ")

     if (len(date_spliited) != 1):
          for i in date_spliited:
               if ((len(i) == 1) or len(i) == 5):
                    i = "0" + i
               dates.append(i)

          date = " - ".join(dates)
          if (len(i) == 3):
               date = date.replace(" - ", " ")
     date = " ".join(date.split()) + " " + year

     return date


def check_event(date, event, START, EXCLUDE, END, NORMAL):
     date_spliited = date.split(" - ")

     if (event.find("before") != -1) or (event.find("exams preparation break") != -1):
          full_month = date.split()[1]
          date = full_months(date, full_month)

          if (date != None):
               month = date[4:6]
               before_result = before(date, event, month)

               if (before_result != None):
                    EXCLUDE.append(before_result)
     elif (len(date_spliited) == 1):
          full_month = date.split()[1]
          if (len(date) != 8):
               date = full_months(date, full_month)

          if (event.find("classes begin") != -1):
               START.append(date)
          elif (event.find("last day of classes") != -1):
               END.append(date)

               if (event.find("normal") != -1):
                    normal_result = normal(date, event)
                    NORMAL.append(normal_result)
          elif (event.find("resume") != -1):
               resume_date = date
               resume(resume_date, date, EXCLUDE)
          elif ((event.find("holiday") != -1) or (event.find("break") != -1) or (event.find("vacation") != -1)):
               EXCLUDE.append(date)
     else:
          if ((event.find("holiday") != -1) or (event.find("break") != -1) or (event.find("vacation") != -1)):
               first_element = date_spliited[0]
               second_element = date_spliited[1]

               if (len(first_element) == 2):
                    full_month = second_element.split()[1]
                    month = (full_months(date, full_month))[4:6]
                    year = date[-4:]

                    day = int(first_element)
                    last_day = int(second_element[0:2]) + 1

                    exclude_range(day, last_day, month, EXCLUDE ,year)
               elif (len(first_element) == 6):
                    first_month = date.split()[1]
                    second_month = date.split()[4]

                    first_element = full_months(first_element, first_month)
                    second_element = full_months(second_element, second_month)
                    date = (second_element + " - " + first_element)

                    two_months(date, EXCLUDE)
               elif (len(first_element) == 11):
                    print(date)

     return START, END, EXCLUDE, NORMAL


def full_months(date, full_month):
     if (len(full_month) == 3):
          index = str(int(days[1].index(full_month)) + 1)

          if (len(index) == 1):
               index = "0" + index
          date = date.replace(full_month, "%s" %index)
          date = "".join(date.split()[::-1])

          return date


def get_days():
     week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

     months = ["JAN", "FAB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
     months_days = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

     return week, months, months_days
days = get_days()


def before(date, event, month):
     if (event.find("last") != -1):
          month_days = int(days[2][int(month) - 1])
          date = int(date) + 1
          day = date%100

          if (month_days < day):
               date = date + 1 - day
               date += 100
          date = str(date)

          return date


def normal(date, event):
     for i in days[0]:
          if (event.find(i) != -1):
               normal_day = (date + ":" + i.upper())
               break

     return normal_day


def resume(resume_date, date, EXCLUDE):
     exclude_date = EXCLUDE[-1]

     if (exclude_date[4:6] == resume_date[4:6]):
          date = date[0:6]
          day = int(exclude_date[6::]) + 1
          last_day = int(resume_date[6::])

          for i in range(day, last_day):
               i = str(i)

               if (len(i) == 1):
                    i = "0" + i
               EXCLUDE.append(date + i)
     else:
          year = date.replace(" ", "")[0:4]

          for i in (0,1):
               if (i == 0):
                    day = int(exclude_date[-2:]) + 1
                    month = exclude_date[4:6]
                    index = int(month) - 1
                    last_day = int(days[2][index]) + 1
               else:
                    day = 1
                    month = resume_date[4:6]
                    last_day = int(resume_date[-2:])

               for j in range(day, last_day):
                    j = str(j)
                    if (len(j) == 1):
                         j = "0" + j
                    EXCLUDE.append(year + month + j)

     return EXCLUDE


def exclude_range(day, last_day, month, EXCLUDE ,year):
     for i in range(day, last_day):
          i = str(i)
          if (len(i) == 1):
               i = "0" + i
          EXCLUDE.append(year + month + i)


def two_months(date, EXCLUDE):
     year = date[0:4]
     dates = date[4:].split(" - ")[::-1]

     for i in (0,1):
          month_element = dates[i]

          if (i == 0):
               day = int(month_element[2::])
               month = month_element[0:2]
               index = int(month) - 1
               last_day = int(days[2][index]) + 1
          else:
               day = 1
               month = month_element[0:2]
               last_day = int(month_element[2::]) + 1

          for j in range(day, last_day):
               j = str(j)
               if (len(j) == 1):
                    j = "0" + j
               EXCLUDE.append(year + month + j)


def main():
     get_term()
main()

print(json.dumps(dictionary))








































import sys
import requests
from bs4 import BeautifulSoup
import json


def dictionary_func(dictionary={}):

     return dictionary


def get_arguments():
     if (len(sys.argv) != 1):
          argv_list = []
          argvs = sys.argv[1::]

          for argv in argvs:
               argv_list.append(argv)

          argvs.sort(reverse=True)
     else:
          argv_list = None

     return argv_list


def get_current_url():
     url = ("https://registrar.kfupm.edu.sa/academic-calendar/current-academic-year/")

     return url


def get_future_url():
     url = ("https://registrar.kfupm.edu.sa/academic-calendar/future-academic-years/")

     return url


def get_past_url():
     url = ("https://registrar.kfupm.edu.sa/academic-calendar/past-academic-years/")

     return url


def get_terms():
     current_url = get_current_url()
     future_url = get_future_url()
     past_url = get_past_url()

     for url in (future_url, current_url, past_url):
          html = requests.get(url).content
          soup = BeautifulSoup(html, 'html.parser')

          options = soup.find_all('option')
          if (len(options) == 2):
               continue

          get_options(soup)


def get_ids():
     ids = ["academic_calendar_option", "academic_calendar_prep_year_option"]

     return ids


def get_options(soup):
     ids = get_ids()

     for id in ids:
          id_index = ids.index(id)
          acad = soup.find(id=id)
          options = acad.find_all('option')[1::]

          get_values(options, id_index)


def get_api_paths():
     api_paths = [["academic-calendar"], ["academic-prep-calendar-first-half", "academic-prep-calendar-second-half"]]

     return api_paths


def get_values(options, id_index):
     years = get_arguments()
     api_paths = get_api_paths()
     api_path_index = api_paths.index(api_paths[id_index])

     for api_path in api_paths[id_index]:
          path_index = api_paths[id_index].index(api_path)

          for option in options:
               value = option["value"]

               if (years == None):
                    term = get_dictionary(value)
                    path = dictionary_path(term, api_path_index, path_index)
                    get_response(api_path, value, path)
               else:
                    for year in years:
                         if (value[0:4] == year):
                              term = get_dictionary(value)
                              path = dictionary_path(term, api_path_index, path_index)
                              get_response(api_path, value, path)


def get_dictionary(value):
     dictionary = dictionary_func()

     term = value[2:5]
     keys = " ".join(list(dictionary.keys()))

     if (keys.find(term) != -1):
          dictionary[term]["prep"] = {"first_half":{},"second_half":{}}
     else:
          dictionary[term] = {}
          dictionary[term]["acad"] = {}

     dictionary_func(dictionary)

     return term


def dictionary_path(term, api_path_index, path_index):
     dictionary = dictionary_func()

     if (api_path_index == 0):
          path = dictionary[term]["acad"]
     else:
          if (path_index == 0):
               half = "first_half"
          else:
               half = "second_half"
          path = dictionary[term][half]

     return path

def get_response(api_path, value, path):
     url = (f"https://registrar.kfupm.edu.sa/api/{api_path}?term_code={value}")
     response = requests.get(url).content
     response_json = json.loads(response)

     get_events(response_json, path)


def get_events(response_json, path):
     events_list = response_json["events"]

     for event in events_list:
          check_event(event, path)


def check_event(event, path):
     exclude_list = []
     normal_list = []

     event_label = (event["event"]).lower()
     start_date = event["start_date"]
     end_date = event["end_date"]

     start_date = get_date(start_date)
     if (end_date != None):
          end_date = get_date(end_date)


     if (event_label.find("exams preparation break") != -1):
          return
     elif (event_label.find("classes begin") != -1):
          start = start_date
          path["start"] = start
     elif (event_label.find("last day of classes") != -1):
          end = start_date
          path["end"] = end

          if (event_label.find("normal") != -1):
               normal_result = normal(start_date, event_label)
               normal_list.append(normal_result)
     elif (event_label.find("last day before") != -1):
          before_result = before(start_date)
          exclude_list.append(before_result)
     elif (event_label.find("nomral") != -1):
          normal_result = normal(start_date, event)
          normal_list.append(normal_result)
     elif (event_label.find("resume") != -1):
          resume(start_date, exclude_list)
     elif ((event_label.find("holiday") != -1) or (event_label.find("break") != -1) or (event_label.find("vacation") != -1)):
          exclude_list.append(start_date)
          if (end_date != None):
               print(end_date)
     else:
          return

     path["exclude"] = exclude_list
     path["normal"] = normal_list

     exclude_list = []
     normal_list = []


def months_func():
     months = ["Jan", "Fab", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
     month_days = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

     return months, month_days


def get_date(date):
     months = months_func()
     month_names_list = months[0]

     month = date[0:3]
     index = month_names_list.index(month)
     str_index = str(index + 1)

     if (index < 10):
          month_index = f"0{str_index}"

     date = date.replace(month_names_list[index], month_index).replace(".", "")
     date = "".join((date).split(", ")[::-1])

     return date


def range():
     pass


def week_days():
     week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

     return week


def normal(date, event):
     week = week_days()

     for day in week:
          if (event.find(day) != -1):
               day = day.lower()
               normal_day = (f"{date}:{day}")

               return normal_day


def resume(date, exclude_list):
     exclude_date = exclude_list[-1]

     if (exclude_date[4:6] == date[4:6]):
          date = date[0:6]
          day = int(exclude_date[6::]) + 1
          last_day = int(resume_date[6::])

          for i in range(day, last_day):
               i = str(i)

               if (len(i) == 1):
                    i = "0" + i
               exclude_list.append(date + i)
     else:
          year = date.replace(" ", "")[0:4]

          for i in (0,1):
               if (i == 0):
                    day = int(exclude_date[-2:]) + 1
                    month = exclude_date[4:6]
                    index = int(month) - 1
                    last_day = int(days[2][index]) + 1
               else:
                    day = 1
                    month = resume_date[4:6]
                    last_day = int(resume_date[-2:])

               for j in range(day, last_day):
                    j = str(j)
                    if (len(j) == 1):
                         j = "0" + j
                    exclude_list.append(year + month + j)

     return exclude_list


def before(date):
     months = months_func()
     month_days = months[1]

     month = int(date[4:6])

     days = int(month_days[int(month) - 1])
     date = int(date) + 1
     day = date%100

     if (days < day):
          date = date + 1 - day
          date += 100

     date = str(date)

     return date


def exclude():
     pass


def main():
     get_terms()
main()


print(dictionary_func())