import sys
import requests
import ast
from bs4 import BeautifulSoup
import json


def get_arguments():
     if (len(sys.argv) != 1):
          argv_list = []
          argvs = sys.argv[1::]

          for argv in argvs:
               argv_list.append(argv)
          argvs.sort(reverse=True)
     else:
          argv_list = ["2021"]

     return argv_list


def get_urls(index):
     def current_url():
          url = ("https://registrar.kfupm.edu.sa/CurrentAcadYear")
          return url

     def past_url():
          url = ("https://registrar.kfupm.edu.sa/PastAcadYear")
          return url

     if (index == 0):
          return current_url()
     elif (index == 1):
          return past_url()


def get_payloads(index):
     def current_payload():
          current_acad = ast.literal_eval(open("payloads/current/acad.json").read())
          current_prep = ast.literal_eval(open("payloads/current/prep.json").read())
          return current_acad, current_prep

     def past_payload():
          past_acad = ast.literal_eval(open("payloads/past/acad.json").read())
          past_prep = ast.literal_eval(open("payloads/past/prep.json").read())
          return past_acad, past_prep

     if (index == 0):
          return current_payload()
     elif (index == 1):
          return past_payload()


def get_halfs():
     halfs = ["FIRST", "SECOND"]

     return halfs
halfs = get_halfs()


def get_replacement():
     replace_from = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "."]
     replace_to = ["JAN", "FAB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

     return replace_from, replace_to


def get_days():
     week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

     months = ["JAN", "FAB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
     months_days = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

     return week, months, months_days
days = get_days()


def get_terms(index):
     years = get_arguments()

     current_acad = []
     current_prep = []
     past_acad = []
     past_prep = []

     for i in (0,1):
          url = get_urls(i)
          payloads = get_payloads(i)

          for payload in payloads:
               html = (requests.post(url, data=payload)).text
               soup = BeautifulSoup(html, 'html.parser')
               options = soup.find_all('option')[1::]

               for option in options:
                    value = option["value"]

                    if (years != None):
                         for year in years:
                              if (value.find(year) != -1):
                                   if (url.find("Current") != -1):
                                        if (option.text.find("Prep") != -1):
                                             current_prep.append(value)
                                        else:
                                             current_acad.append(value)
                                   elif (url.find("Past") != -1):
                                        if (option.text.find("Prep") != -1):
                                             past_prep.append(value)
                                        else:
                                             past_acad.append(value)
                    else:
                         if (url.find("Current") != -1):
                              if (option.text.find("Prep") != -1):
                                   current_prep.append(value)
                              else:
                                   current_acad.append(value)
                         elif (url.find("Past") != -1):
                              if (option.text.find("Prep") != -1):
                                   past_prep.append(value)
                              else:
                                   past_acad.append(value)

     if (index == 0):
          return current_acad, current_prep
     elif (index == 1):
          return past_acad, past_prep


def get_tables():
     tables = []

     for i in (0,1):
          url = get_urls(i)
          payloads = get_payloads(i)
          terms = get_terms(i)

          for j in (0,1):
               payload = payloads[j]
               page_term = terms[j]
               last_key = list(payload.keys())[-1]

               for term in page_term:
                    payload[last_key] = term
                    html = (requests.post(url, data = payload)).text
                    soup = BeautifulSoup(html, 'html.parser')
                    term_tables = soup.find_all(class_ = "table-responsive")
                    tables.append(term_tables)

     return tables
tables = get_tables()


def get_terms_dictionary():
     dictionary = {}

     for table in tables:
          soup = BeautifulSoup(str(table), 'html.parser')

          if (len(soup.text) != 4):
               pdf_href = soup.find("a").get("href")
               href_splitted = pdf_href.replace("_", "/").replace(".", "/").split("/")
               neede_elements = href_splitted[4:len(href_splitted)-1]
               term = neede_elements[0][2:5]

               keys = " ".join(list(dictionary.keys()))

               if (keys.find(term) != -1):
                    dictionary[term]["PREP"] = {"FIRST":{},"SECOND":{}}
               else:
                    dictionary[term] = {}
                    dictionary[term]["ACAD"] = {}

     return dictionary
terms_dictionary = get_terms_dictionary()


def get_organized_events():
     for table in tables:
          soup = BeautifulSoup(str(table), 'html.parser')
          pdf_href = soup.find("a").get("href")
          href_splitted = pdf_href.replace("_", "/").replace(".", "/").split("/")
          neede_elements = href_splitted[4:len(href_splitted)-1]
          term = neede_elements[0][2:5]

          if (len(neede_elements) != 3):
               dictionary = terms_dictionary[term]["ACAD"]
          else:
               dictionary = terms_dictionary[term]["PREP"]

          for half in table:
               TABLE = []

               soup = BeautifulSoup(str(half), 'html.parser')
               index = table.index(half)

               if (index == 1 and len(neede_elements) != 3):
                    continue
               elif (len(neede_elements) == 3):
                    dictionary = terms_dictionary[term]["PREP"][halfs[index]]

               columns = soup.find_all("tr")[1::]

               for column in columns:
                    rows = column.find_all('td')

                    if (len(rows) == 4):
                         row = 2
                    else:
                         row = 3

                    full_date = " ".join(((rows[row].text).lower()).split())
                    event = " ".join(((rows[row + 1].text).lower()).split())
                    TABLE.append(full_date + ", " + event)

               dictionary["TABLE"] = TABLE
get_organized_events()


def full_dates():
     replacement = get_replacement()

     for term in terms_dictionary:
          term_path = terms_dictionary[term]

          for acad_prep in term_path:
               tables = []
               first_line = False

               if (acad_prep.find("ACAD") != -1):
                    tables.append(term_path[acad_prep]["TABLE"])
                    dictionary = terms_dictionary[term][acad_prep]
                    del term_path[acad_prep]["TABLE"]
               elif (acad_prep.find("PREP") != -1):
                    prep = False
                    for i in (0,1):
                         dictionary = terms_dictionary[term]["PREP"][halfs[i]]
                         tables.append(terms_dictionary[term]["PREP"][halfs[i]])

               dictionary = terms_dictionary[term][acad_prep]

               for table in tables:
                    TABLE = []
                    if (acad_prep.find("PREP") != -1):
                         table = table["TABLE"]
                         if (prep == False):
                              index = 0
                              prep = True
                         else:
                              index = 1

                         dictionary = terms_dictionary[term]["PREP"][halfs[index]]


                    for date_event in table:
                         dates = []

                         splitted = date_event.split(", ")
                         full_date = splitted[0]
                         event = splitted[1]

                         for i in range(39):
                              full_date = full_date.replace(str(replacement[0][i]), str(replacement[1][i]))

                         if (first_line == False):
                              splitted_full_date = full_date.replace("'", " ").replace("-", " ").split()
                              year = splitted_full_date[-1]
                              if (len(year) == 2):
                                   year = "20" + year
                              next_year = str(int(year) + 1)
                              first_line = True
                         elif (full_date.find(next_year) != -1):
                              year = next_year

                         if ((full_date.find("DEC") != -1) and (full_date.find("JAN") != -1)):
                              splitted_full_date = " ".join(full_date.replace("-", " - ").split()).split(" - ")

                              for i in splitted_full_date:
                                   if (len(i) == 10):
                                        i = "0" + i
                                   splitted = i.split("'")

                                   if (len(splitted) == 1):
                                        dates.append(splitted[0])

                                        if (len(dates) == 2):
                                             full_date = dates[1]
                                             year = str(int(full_date[7:11]) - 1)
                                             dates[0] = dates[0] + " " + year
                                   else:
                                        dates.append(splitted[0] + " 20" + splitted[1])

                              full_date = " - ".join(dates)
                         elif (full_date.find(year) != -1):
                              full_date = " ".join(full_date.replace("%s" %year, "").split())
                              if (full_date[-1].find("-") != -1):
                                   full_date = full_date.replace("-", " ")
                              elif (len(full_date) == 5 or len(full_date) == 6):
                                   full_date = full_date.replace("-", " ")

                              splitted_full_date = " ".join(full_date.replace("-", " - ").split()).split(" - ")
                              if (len(splitted_full_date) != 1):
                                   for i in splitted_full_date:
                                        if ((len(i) == 1) or len(i) == 5):
                                             i = "0" + i
                                        dates.append(i)

                                   full_date = " - ".join(dates)
                              full_date = " ".join(full_date.split()) + " " + year
                         else:
                              splitted_full_date = " ".join(full_date.replace("-", " - ").split()).split(" - ")
                              if (len(splitted_full_date) != 1):
                                   for i in splitted_full_date:
                                        if ((len(i) == 1) or len(i) == 5):
                                             i = "0" + i
                                        dates.append(i)

                                   full_date = " - ".join(dates)
                                   if (len(i) == 3):
                                        full_date = full_date.replace(" - ", " ")
                              full_date = " ".join(full_date.split()) + " " + year

                         if (len(full_date) == 10):
                              full_date = "0" + full_date
                         TABLE.append(full_date + ", " + event)
                    dictionary["TABLE"] = TABLE
full_dates()


def main():
     for terms in terms_dictionary:
          term = terms_dictionary[terms]
          for acad_prep in term:
               table = term[acad_prep]["TABLE"]
               del term[acad_prep]["TABLE"]

               dictionary = terms_dictionary[terms][acad_prep]
               NORMAL = []
               INCLUDE = []
               EXCLUDE = []
               for date_event in table:
                    splitted = date_event.split(", ")
                    full_date = splitted[0]
                    event = splitted[1]

                    splitted_full_date = full_date.split(" - ")
                    if (event.find("last day before") != -1) or (event.find("exams preparation break") != -1):
                         continue
                    elif (len(splitted_full_date) == 1):
                         full_month = full_date.split()[1]
                         if (len(full_month) == 3):
                              index = str(int(month[0].index(full_month)) + 1)
                              full_date = full_date.replace(full_month, "0%s" %index)
                              full_date = "".join(full_date.split()[::-1])

                         if ((event.find("classes begin") != -1) or (event.find("last day of classes") != -1) or (event.find("normal") != -1)):
                              INCLUDE.append(full_date)
                              if (event.find("normal") != -1):
                                   EXCLUDE.append(full_date)
                                   for i in days_weeks:
                                        if (event.find(i) != -1):
                                             NORMAL.append(full_date + ":" + i.upper())
                         elif (event.find("resume") != -1):
                              print(date_event)
                         elif ((event.find("holiday") != -1) or (event.find("break") != -1)):
                              EXCLUDE.append(full_date)
                    else:
                         if ((event.find("holiday") != -1) or (event.find("break") != -1)):
                              first_element = splitted_full_date[0]
                              second_element = splitted_full_date[1]
                              if (len(first_element) == 2):
                                   full_month = full_date.split()[3]
                                   index = str(int(month[0].index(full_month)) + 1)
                                   full_date = full_date.replace(full_month, "0%s" %index)
                                   full_date = "".join((full_date.split()[2::])[::-1])
                                   for i in range(int(first_element), int(second_element[0:2]) + 1):
                                        i = str(i)
                                        if (len(i) == 1):
                                             i = "0" + i
                                        EXCLUDE.append(full_date + i)
                              elif (len(first_element) == 6):
                                   pass
                              elif (len(first_element) == 11):
                                   pass
                              print(splitted_full_date)



               print(EXCLUDE)
               print(INCLUDE)
               print(NORMAL)
               print()


















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

# main2()