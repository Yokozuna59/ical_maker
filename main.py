# import modules
import requests
import ast
from bs4 import BeautifulSoup

# create the URL variable
url = ("https://registrar.kfupm.edu.sa/CurrentAcadYear")

# create lists for the replacement loop
replace_from = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
replace_to = ["/1", "/2", "/3", "/4", "/5", "/6", "/7", "/8", "/9", "/10", "/11", "/12", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
# create lists for the check loop
event_check = ["classes begin", "holiday", "resume", "break", "normal", "last day of classes"]

# open and read the payloads.txt file
payloads = open("payloads.txt", "r").read()
splitted_payloads = payloads.split("~~~")

for i in range(len(splitted_payloads)):
     payload = ast.literal_eval(splitted_payloads[i])
     html = (requests.post(url, data = payload)).text
     soup = BeautifulSoup(html, 'html.parser')

     # create a list to add the terms
     registrar_terms = []
     options_of_terms = soup.find_all('option')
     for j in options_of_terms:
          if (j["value"].find("0") != 0):
               registrar_terms.append(j["value"])

     for j in registrar_terms:
          first_line = False
          short_term = j[2:5]
          terms = []

          key = list(payload.keys())[-1]
          payload[key] = j
          html = (requests.post(url, data = payload)).text
          soup = BeautifulSoup(html, 'html.parser')
          table = soup.find(class_ = "table table-striped")
          table_rows = table.find_all("tr")

          for k in table_rows:
               elements = k.find_all('td')
               if (len(elements) != 0):
                    date = " ".join(((elements[3].text).lower()).split())
                    for k in range(len(replace_from)):
                         date = date.replace(replace_from[k], replace_to[k])
                    event = " ".join(((elements[4].text).lower()).split())

                    if (first_line == False):
                         splitted_date = date.replace("-", " ").split()
                         year = splitted_date[-1]
                         next_year = str(int(year) + 1)
                         first_line = True

                    if (date.find(next_year) != -1):
                         year = next_year
                         year_change = True

                    if (event.find("last day before") != -1) or (event.find("exams preparation break") != -1):
                         continue
                    elif (event.find("classes begin") != -1) or(event.find("holiday") != -1) or (event.find("resume") != -1) or (event.find("break") != -1) or (event.find("normal") != -1) or (event.find("last day of classes") != -1):
                         splitted_date = (date.replace("%s" %year, "/" + year).replace("%s" %next_year, "/" + next_year)).split()
                         dates = []

                         for m in splitted_date:
                              if (year == m):
                                   dates.append("".join("/" + m))
                              else:
                                   dates.append(m)
                              date = "".join(dates)
                              if (date.find(year) != -1) or (date.find(next_year) != -1):
                                   pass
                              else:
                                   date = "".join(date + "/" + year)
                         terms.append(date + ", " + event)

          print(terms[0])
          print(terms[-1])
          print(short_term, end="")
          print(" = ", end= "")
          print(terms)