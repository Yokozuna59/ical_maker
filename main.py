# import modules
import requests
import ast
from bs4 import BeautifulSoup
import json

def get_urls():
     urls = ["https://registrar.kfupm.edu.sa/CurrentAcadYear", "https://registrar.kfupm.edu.sa/PastAcadYear"]
     return urls


def get_payloads():
     current_acad = ast.literal_eval(open("payloads/current/acad.json").read())
     current_prep = ast.literal_eval(open("payloads/current/prep.json").read())

     past_acad = ast.literal_eval(open("payloads/past/acad.json").read())
     past_prep = ast.literal_eval(open("payloads/past/prep.json").read())
     return current_acad, current_prep, past_acad, past_prep


def get_terms():
     urls = get_urls()
     payloads = get_payloads()

     current_acad_terms = []
     current_prep_terms = []
     past_acad_terms = []
     past_prep_terms = []

     for url in urls:
          for payload in payloads:
               html = (requests.post(url, data=payload)).text
               soup = BeautifulSoup(html, 'html.parser')
               options = soup.find_all('option')

               for option in options:
                    if (option["value"].find("0") != 0):
                         if (url.find("Current") != -1):
                              if (option.text.find("Prep") != -1):
                                   current_prep_terms.append(option["value"])
                              else:
                                   current_acad_terms.append(option["value"])
                         elif (url.find("Past") != -1):
                              if (option.text.find("Prep") != -1):
                                   past_prep_terms.append(option["value"])
                              else:
                                   past_acad_terms.append(option["value"])
     return current_acad_terms, current_prep_terms, past_acad_terms, past_prep_terms


def table():
     urls = get_urls()
     terms = get_terms()
     payloads = get_payloads()

     for url in urls:
          for index_payload in range(len(payloads)):
               for page in range(len(terms)):
                    if (url.find("Current") != -1):
                         if (page == 2):
                              break
                    elif (url.find("Past") != -1):
                         page = 2
                         index_payload = 2
                    if (page == index_payload):
                         payload = payloads[index_payload]
                         last_key = list(payload.keys())[-1]
                         for i in list(terms[page]):
                              payload[last_key] = i
                              html = (requests.post(url, data = payload)).text
                              soup = BeautifulSoup(html, 'html.parser')
                              table = soup.find_all(class_ = "table-responsive")
                              print(table)

table()






def days_month(month):
     days_month = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]
     return days_month[month]


def main2():
     url = ("https://registrar.kfupm.edu.sa/currentacadyear")

     # create lists
     halfs = ["FIRST", "SECOND"] # list for the "FIRST" and "SECOND" halfs

     # create two lists for the replacement loop
     replace_from = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
     replace_to = ["01/", "02/", "03/", "04/", "05/", "06/", "07/", "08/", "09/", "10/", "11/", "12/", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

     academic_prep = ["ACAD", "PREP"] # list for the "ACAD" and "PREP" years

     days_of_month = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

     include_exlucde = ["INCLUDE", "EXCLUDE"] # list for the "INCLUDE" and "EXCLUDE" dates

     # open and read the "payloads.txt" file then split split it by "~~~"
     payloads = open("payloads.txt", "r").read()
     splitted_payloads = payloads.split("~~~")

     # for loop with "Academic" and "Prep" years payloads
     for i in range(len(splitted_payloads)):
          # create a list to add the terms from registrar page
          registrar_terms = []

          # get the element and convert it to dictionary then post the request and scrap the page
          payload = ast.literal_eval(splitted_payloads[i])
          html = (requests.post(url, data = payload)).text
          soup = BeautifulSoup(html, 'html.parser')

          # get the options of terms and add it to the list
          options_of_terms = soup.find_all('option')
          for j in options_of_terms:
               if (j["value"].find("0") != 0):
                    registrar_terms.append(j["value"])

          # for loop with terms from registrar
          for j in registrar_terms:
               # get the last key from payload then assign new value for it and scrap the page
               last_key = list(payload.keys())[-1]
               payload[last_key] = j
               html = (requests.post(url, data = payload)).text
               soup = BeautifulSoup(html, 'html.parser')

               # get all classes with "table-responsive" then use it in for loop
               table = soup.find_all(class_ = "table-responsive")
               for k in range(len(table)):
                    # ignore the empty table
                    if (len(table[k].text) != 4):
                         # create a bool variable to check if the first line have been checked yet or not
                         first_line = False

                         # create empty lists to the included and excluded dates
                         needed_events = []
                         excluded_dates = []
                         included_dates = []

                         # create the short name term variable, e.g. "211"
                         short_term = j[2:5]

                         # creat a full term variable
                         term = academic_prep[i] + short_term

                         # check if i is 0 == ACAD, 1 == PREP
                         if (i == 1):
                              term += halfs[k]

                         # get the table's columns and use it in the for loop
                         columns = table[k].find_all("tr")
                         for k in columns:
                              # get the column rows and get the needed ones
                              rows = k.find_all('td')

                              # ignore the empty row
                              if (len(rows) != 0):
                                   # get the full date and event then make them lowercase then remove double space
                                   full_date = " ".join(((rows[3].text).lower()).split())
                                   event = " ".join(((rows[4].text).lower()).split())

                                   # use the current index and replace word from the replacement lists
                                   for k in range(len(replace_from)):
                                        full_date = full_date.replace(replace_from[k], replace_to[k])

                                   # check the first line bool statement
                                   if (first_line == False):
                                        splitted_full_date = full_date.split()
                                        year = splitted_full_date[-1]
                                        next_year = str(int(year) + 1)
                                        first_line = True
                                   elif (full_date.find(next_year) != -1):
                                        year = next_year

                                   # ignore if the event contains "last day before" and "exams preparation break"
                                   if (event.find("last day before") != -1) or (event.find("exams preparation break") != -1):
                                        continue
                                   # check if the event contains the key words for the needed events
                                   elif (event.find("classes begin") != -1) or(event.find("holiday") != -1) or (event.find("resume") != -1) or (event.find("break") != -1) or (event.find("normal") != -1) or (event.find("last day of classes") != -1):
                                        # split full date with spaces
                                        splitted_full_date = (full_date.replace("-", " - ").split())

                                        # create an empty list to add elements of splitted full date
                                        dates = []

                                        # get elements from the splitted full date reversed: (YEAR, MONTH, DAY)
                                        for k in splitted_full_date[::-1]:
                                             # check if full date contains (year)
                                             if (year == k):
                                                  dates.append(k)
                                             else:
                                                  if ((len(k) == 1) and (k != "-")):
                                                       k = '0' + k
                                                  dates.append(k)

                                             full_date = "".join(dates)
                                             if (full_date.find(year) != -1):
                                                  pass
                                             else:
                                                  full_date = "".join(year + full_date)

                                        if ((full_date.find("-") != -1) or event.find("resume") != -1):
                                             split_by_slash = (" ".join((" ".join(full_date[4::].split("/"))).split("-")).split())[::-1]
                                             if (len(split_by_slash) == 2):
                                                  before_resume = (needed_events[-1].split(", "))
                                                  day_before_resume = before_resume[0][6::]
                                                  month_before_resume = before_resume[0][4:6]
                                                  event_before_resume = before_resume[1]

                                                  month = split_by_slash[1]
                                                  if (month_before_resume == month):
                                                       for k in range(int(day_before_resume) + 1, int(split_by_slash[0])):
                                                            k = str(k)
                                                            if ((len(k) == 1)):
                                                                 k = '0' + k
                                                            needed_events.append(full_date[0:6] + k + ", " + event_before_resume)
                                                  else:
                                                       for k in (0,1):
                                                            if (k == 0):
                                                                 month = month_before_resume
                                                                 days = day_before_resume
                                                                 month_days = days_of_month[int(month_before_resume) - 1]
                                                            else:
                                                                 month = split_by_slash[1]
                                                                 days = 1
                                                                 month_days = split_by_slash[0]

                                                            for k in range(int(days) + 1, int(month_days) + 1):
                                                                 k = str(k)
                                                                 if ((len(k) == 1)):
                                                                      k = '0' + k
                                                                 needed_events.append(full_date[0:4] + month + k + ", " + event_before_resume)
                                                  full_date = full_date.replace("/", "")
                                                  needed_events.append(full_date + ", " + event)

                                             elif len(split_by_slash) == 3:
                                                  for k in range(int(split_by_slash[0]), int(split_by_slash[1]) + 1):
                                                       k = str(k)
                                                       if ((len(k) == 1)):
                                                            k = '0' + k
                                                       needed_events.append(full_date[0:6] + k + ", " + event_before_resume)
                                             elif (len(split_by_slash) == 4):
                                                  for k in (0,2):
                                                       month = split_by_slash[k + 1]
                                                       if (k == 2):
                                                            days = 1
                                                            month_days = split_by_slash[k]
                                                       else:
                                                            days = split_by_slash[k]
                                                            month_days = days_of_month[int(month) - 1]

                                                       for k in range(int(days) , int(month_days) + 1):
                                                            k = str(k)
                                                            if ((len(k) == 1)):
                                                                 k = '0' + k
                                                            needed_events.append(full_date[0:4] + month + k + ", " + event)
                                        else:
                                             full_date = full_date.replace("/", "")
                                             needed_events.append(full_date + ", " + event)

                         for m in needed_events:
                              if ((m.find("classes begin") != -1) or (m.find("resume") != -1) or (m.find("last day of classes") != -1)):
                                   included_dates.append(m)
                              else:
                                   print
                                   excluded_dates.append(m)

                         print(term, end=" INCLUDE")
                         print(" = ", end= "")
                         print(included_dates)
                         print(term, end=" EXCLUDE")
                         print(" = ", end= "")
                         if (len(excluded_dates) == 0):
                              print(None)
                         else:
                              print(excluded_dates)