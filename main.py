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
          argv_list = None

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
               page_terms = terms[j]
               last_key = list(payload.keys())[-1]

               for term in page_terms:
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
                         half = halfs[index]

                         dictionary = terms_dictionary[term]["PREP"][half]


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
     for term in terms_dictionary:
          term_path = terms_dictionary[term]

          for acad_prep in term_path:
               tables = []

               if (acad_prep.find("ACAD") != -1):
                    tables.append(term_path[acad_prep]["TABLE"])
                    del term_path[acad_prep]["TABLE"]
               elif (acad_prep.find("PREP") != -1):
                    prep = False
                    for i in (0,1):
                         dictionary = terms_dictionary[term]["PREP"][halfs[i]]
                         tables.append(terms_dictionary[term]["PREP"][halfs[i]])

               dictionary = terms_dictionary[term][acad_prep]
               for table in tables:
                    if (acad_prep.find("PREP") != -1):
                         table = table["TABLE"]
                         if (prep == False):
                              index = 0
                              prep = True
                         else:
                              index = 1
                         half = halfs[index]

                         dictionary = terms_dictionary[term]["PREP"][half]
                         del terms_dictionary[term]["PREP"][half]["TABLE"]

                    START = []
                    END = []
                    NORMAL = []
                    EXCLUDE = []

                    for date_event in table:
                         splitted = date_event.split(", ")
                         full_date = splitted[0]
                         event = splitted[1]

                         splitted_full_date = full_date.split(" - ")
                         if (event.find("before") != -1) or (event.find("exams preparation break") != -1):
                              full_month = full_date.split()[1]
                              if (len(full_month) == 3):
                                   index = str(int(days[1].index(full_month)) + 1)
                                   if (len(index) == 1):
                                        index = "0" + index
                                   full_date = full_date.replace(full_month, "%s" %index)
                                   full_date = "".join(full_date.split()[::-1])

                              if (event.find("last") != -1):
                                   full_date = str(int(full_date) + 1)
                                   EXCLUDE.append(full_date)

                         elif (len(splitted_full_date) == 1):
                              full_month = full_date.split()[1]
                              if (len(full_month) == 3):
                                   index = str(int(days[1].index(full_month)) + 1)
                                   if (len(index) == 1):
                                        index = "0" + index
                                   full_date = full_date.replace(full_month, "%s" %index)
                                   full_date = "".join(full_date.split()[::-1])

                              if (event.find("classes begin") != -1):
                                   START.append(full_date)
                              elif (event.find("last day of classes") != -1):
                                   END.append(full_date)
                                   if (event.find("normal") != -1):
                                        EXCLUDE.append(full_date)
                                        for i in days[0]:
                                             if (event.find(i) != -1):
                                                  NORMAL.append(full_date + ":" + i.upper())
                              elif (event.find("normal") != -1):
                                   EXCLUDE.append(full_date)
                                   for i in days[0]:
                                        if (event.find(i) != -1):
                                             NORMAL.append(full_date + ":" + i.upper())
                              elif (event.find("resume") != -1):
                                   exclude_date = EXCLUDE[-1]
                                   resume_date = full_date

                                   if (exclude_date[4:6] == resume_date[4:6]):
                                        full_date = full_date[0:6]
                                        for i in range(int(exclude_date[6::]) + 1, int(resume_date[6::])):
                                             i = str(i)
                                             if (len(i) == 1):
                                                  i = "0" + i
                                             EXCLUDE.append(full_date + i)
                                   else:
                                        year = full_date.replace(" ", "")[0:4]

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
                              elif ((event.find("holiday") != -1) or (event.find("break") != -1) or (event.find("vacation") != -1)):
                                   EXCLUDE.append(full_date)
                         else:
                              if ((event.find("holiday") != -1) or (event.find("break") != -1) or (event.find("vacation") != -1)):
                                   first_element = splitted_full_date[0]
                                   second_element = splitted_full_date[1]

                                   if (len(first_element) == 2):
                                        full_month = full_date.split()[3]
                                        index = str(int(days[1].index(full_month)) + 1)
                                        if (len(index) == 1):
                                             index = "0" + index
                                        full_date = full_date.replace(full_month, "%s" %index)
                                        full_date = "".join((full_date.split()[3::])[::-1])
                                        for i in range(int(first_element), int(second_element[0:2]) + 1):
                                             i = str(i)
                                             if (len(i) == 1):
                                                  i = "0" + i
                                             EXCLUDE.append(full_date + i)
                                   elif (len(first_element) == 6):
                                        first_month = full_date.split()[1]
                                        second_month = full_date.split()[4]

                                        for i in (first_month, second_month):
                                             index = str(int(days[1].index(i)) + 1)
                                             if (len(index) == 1):
                                                  index = "0" + index
                                             full_date = full_date.replace(i, "%s" %index)
                                        year = full_date[-4:]
                                        dates = full_date.replace(" ", "")[:-4].split("-")

                                        for i in (0,1):
                                             month_element = dates[i]
                                             if (i == 0):
                                                  day = int(month_element[0:2])
                                                  month = month_element[2::]
                                                  index = int(month) - 1
                                                  last_day = int(days[2][index]) + 1
                                             else:
                                                  day = 1
                                                  month = month_element[2::]
                                                  last_day = int(month_element[0:2]) + 1


                                             for j in range(day, last_day):
                                                  j = str(j)
                                                  if (len(j) == 1):
                                                       j = "0" + j
                                                  EXCLUDE.append(year + month + j)
                                   # elif (len(first_element) == 11):
                                   #      print(splitted_full_date)

                    dictionary["START"] = START
                    dictionary["END"] = END
                    dictionary["EXCLUDE"] = EXCLUDE
                    dictionary["NORMAL"] = NORMAL

main()

json_dictionary = json.dumps(terms_dictionary)
print(json_dictionary)