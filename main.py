import sys
import requests
import ast
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


def current():
     url = ("https://registrar.kfupm.edu.sa/CurrentAcadYear")

     acad = ast.literal_eval(open("payloads/current/acad.json").read())
     prep = ast.literal_eval(open("payloads/current/prep.json").read())
     payloads = [acad, prep]

     return url, payloads


def past():
     url = ("https://registrar.kfupm.edu.sa/PastAcadYear")

     acad = ast.literal_eval(open("payloads/past/acad.json").read())
     prep = ast.literal_eval(open("payloads/past/prep.json").read())
     payloads = [acad, prep]

     return url, payloads


def get_term():
     years = get_arguments()

     for i in (current(), past()):
          url = i[0]
          payloads = i[1]

          for payload in payloads:
               html = (requests.post(url, data=payload)).content
               soup = BeautifulSoup(html, 'html.parser')
               options = soup.find_all('option')[1::]

               for option in options:
                    value = option["value"]

                    if (years == None):
                         get_table(url, payload, value)
                    else:
                         for year in years:
                              if (value[0:4] == (year)):
                                   get_table(url, payload, value)


def get_table(url, payload, value):
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
     tables = soup.find_all(class_ = "table-responsive")

     get_dates_events(tables, term)


def get_dates_events(tables, term):
     START = []
     END = []
     NORMAL = []
     EXCLUDE = []

     soup = BeautifulSoup(str(tables[0]), 'html.parser')
     href_pdf = soup.find("a").get("href")
     first_line = False

     if (href_pdf.find("PREP") != -1):
          academic = "PREP"
     else:
          academic = "ACAD"

     for table in tables:
          soup = BeautifulSoup(str(table), 'html.parser')
          path = dictionary[term][academic]

          table_index = tables.index(table)

          if ((academic == "ACAD") and (table_index == 1)):
               continue
          elif ((academic == "PREP")):
               half = get_halfs(table_index)
               path = dictionary[term][academic][half]

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
                    first_element = first_column(date)
                    year = first_element[0]
                    next_year = first_element[1]

                    first_line = True
               elif (date.find(next_year) != -1):
                    year = next_year

               if ((date.find("DEC") != -1) and (date.find("JAN") != -1)):
                    date = two_years(date)
               elif (date.find(year) != -1):
                    date = one_year(date, year)
               else:
                    date = not_1_year_nor_2_year(date, year)

               if (len(date) == 10):
                    date = "0" + date

               check_event(date, event, START, EXCLUDE, END, NORMAL)
          path["START"] = START
          path["END"] = END
          path["EXCLUDE"] = EXCLUDE
          path["NORMAL"] = NORMAL

          START = []
          EXCLUDE= []
          END= []
          NORMAL = []


def get_halfs(table_index):
     halfs = ["FIRST", "SECOND"]
     half = halfs[table_index]

     return half


def replacement(date):
     replace_from = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "."]
     replace_to = ["JAN", "FAB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

     for i in range(39):
          date = date.replace(replace_from[i], replace_to[i])

     return date


def first_column(date):
     date_spliited = date.replace("'", " ").replace("-", " ").split()
     year = date_spliited[-1]

     if (len(year) == 2):
          year = "20" + year

     next_year = str(int(year) + 1)

     return year, next_year


def two_years(date):
     dates = []
     date_spliited = (" ".join(date.replace("-", " - ").split())).split(" - ")

     for i in date_spliited:
          if (len(i) == 10):
               i = "0" + i
          splitted = i.split("'")

          if (len(splitted) == 1):
               dates.append(splitted[0])

               if (len(dates) == 2):
                    date = dates[1]
                    year = str(int(date[7:11]) - 1)
                    dates[0] = dates[0] + " " + year
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


def not_1_year_nor_2_year(date, year):
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
                    EXCLUDE.append(date)
                    normal_result = normal(date, event)
                    NORMAL.append(normal_result)
          elif (event.find("resume") != -1):
               resume_date = date
               resume_result = resume(resume_date, date, EXCLUDE)

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

                    year = date[0:4]
                    dates = date[4:].split(" - ")

                    for i in (0,1):
                         month_element = dates[i]

                         if (i == 0):
                              day = int(month_element[0:2])
                              month = month_element[2::]
                              index = int(month) - 1
                              last_day = int(days[2][index]) + 1
                         else:
                              day = 1
                              month = month_element[0:2]
                              last_day = int(month_element[0:2]) + 1


                         for j in range(day, last_day):
                              j = str(j)
                              if (len(j) == 1):
                                   j = "0" + j
                              EXCLUDE.append(year + month + j)
               elif (len(first_element) == 11):
                    print(date)

     return START, END, EXCLUDE, NORMAL


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


def full_months(date, full_month):
     if (len(full_month) == 3):
          index = str(int(days[1].index(full_month)) + 1)

          if (len(index) == 1):
               index = "0" + index
          date = date.replace(full_month, "%s" %index)
          date = "".join(date.split()[::-1])

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


def main():
     get_term()
main()


json_dictionary = json.dumps(dictionary)
print(json_dictionary)