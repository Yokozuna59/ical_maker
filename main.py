# import modules
import requests
import ast
from bs4 import BeautifulSoup

# create the "url" variable
url = ("https://registrar.kfupm.edu.sa/CurrentAcadYear")

# create two lists for the replacement loop
replace_from = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
replace_to = ["01/", "02/", "03/", "04/", "05/", "06/", "07/", "08/", "09/", "10/", "11/", "12/", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

# create a list for the check loop
event_check = ["classes begin", "holiday", "resume", "break", "normal", "last day of classes"]

# months
months = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]

# create a list for the "Academic" and "Prep" year
academic_prep = ["ACAD ", "PREP "]

# create a list for the "First" and "Second" halfs
halfs = [" FIRST", " SECOND"]

# open and read the payloads.txt file then split split it by "~~~"
payloads = open("payloads.txt", "r").read()
splitted_payloads = payloads.split("~~~")

# do a for loop with "Academic" and "Prep" years
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

     # do a for loop with terms from registrar
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

                    # create an empty list to the needed dates with event
                    needed_events = []

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

                                   if (full_date.find("-") != -1):
                                        split_by_slash = (" ".join((" ".join(full_date[4::].split("/"))).split("-")).split())[::-1]
                                        if len(split_by_slash) == 3:
                                             for k in range(int(split_by_slash[0]), int(split_by_slash[1]) + 1):
                                                  k = str(k)
                                                  if ((len(k) == 1)):
                                                       k = '0' + k
                                                  needed_events.append(full_date[0:6] + k + ", " + event)
                                        else:
                                             print(split_by_slash)
                                             for k in (0,2):
                                                  if (k == 2):
                                                       days = 1
                                                  else:
                                                       days = split_by_slash[k]
                                                  month = split_by_slash[k + 1]
                                                  month_days = months[int(month) - 1]
                                                  for k in range(int(days) , int(month_days) + 1):
                                                       k = str(k)
                                                       if ((len(k) == 1)):
                                                            k = '0' + k
                                                       needed_events.append(full_date[0:4] + month + k + ", " + event)
                                   else:
                                        full_date = full_date.replace("/", "")
                                        needed_events.append(full_date + ", " + event)

                    print(term, end="")
                    print(" = ", end= "")
                    print(needed_events)