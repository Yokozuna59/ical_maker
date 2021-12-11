import requests
from bs4 import BeautifulSoup

# open the registrar current year page then scrap it
url = ("https://registrar.kfupm.edu.sa/CurrentAcadYear")
r = (requests.get(url)).text
soup = BeautifulSoup(r, 'html.parser')

#.replace("-%s" %term, " " + str(term)).replace("-%s" %next_year, " " + str(next_year)).split())
replace_from = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
replace_to = ["/1", "/2", "/3", "/4", "/5", "/6", "/7", "/8", "/9", "/10", "/11", "/12", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

event_check = ["classes begin", "holiday", "resume", "break", "normal", "last day of classes"]
#if (event.find("Last day before") != -1):

registrar_terms = []
choices = soup.find_all('option')
for i in choices:
     if (i["value"].find("0") != 0):
          registrar_terms.append(i["value"])

for i in registrar_terms:
     first_line = False
     short_term = i[2:5]
     terms = []

     payload = {
          "__EVENTTARGET": "ctl00$CntntPlcHldr$ddlAcadClndr",
          "__EVENTARGUMENT": "",
          "__LASTFOCUS": "",
          "__VIEWSTATE": "P4ozIGd1QoCFMmYd7EbMU70iA2h1xh9LIwgZQj4apyIt0BpVoYHcIEOgtXFQ2uW9T9pK98RvlQCj9/wt1lc9Y0Cm3VBph7AFLu8i6p/oSq0iYOG+4SDO0unhEgFcwkaL5Vo3hIqyC2hRZH9Bnkht0nCk9GGb4oiX2yos/C+S3f4xHWQPgdrX7bKvaJT8EO34YbHaMReP3E1l3XKjoS5yVJyeelvy90I3+UKdNjorAIXBlbLR2psiUeCo8TYoMBXMtz4zwDQ98IroaxeQVMuIY5W+UdbKDnYaUKmOrm7wVNWjdxMjJWl1HVug7N+F9tb1YjB8ULUUhle+0HOTCps8SVAtR95W6m3ngWe3B1x7D1eglv9llT9CtQh9/TGwvc/QXA1K92USYl/GK+36evxhbNvYQT+GdDIyefkNXFZYvZx/9zi8xNnbR8INSu08ywYxoBnqhcn2mkrk7qV2VNg707U+iCz7o96mdGz4S3rZ3JwbeZCoWw+7XS4Pf45fb8Pwq57+KFAuUl+yBQwxaWgohyJgOw71/ujkkbmrdYTU5TeV0NqSWuh6D6GnN7uk0enxGHS/fJ23Trosx4I5qNwcZP75sxsa2VA8+VDcwMcQkM29ns0xyUi2izmgwkzP+9TMAEnFYCqITyt6PSIE155V/3+LXkLq9YT60r4ZGMVtAE/vvB53Uf4eda/hFBOZE+C/qQzMTSN7soXHZiOOZtJNqaL2fi5o3ZTF9UVPyltpWZ/ABvOCwDlImhlqXDzEUqR4FbhpZIE2cGZL+0CDCyvLjaDBSxiYOs1ggnnKTC3fg9fI9+ZGxnpWN4CcWcDKv81lpDfnsBGJ4q2cAANs0xvseuAEVR2wp3rE2lZ9MrJUJtj0ZuEWCiQUeeBJE8JL3y7L9SLBn8FGqzFVyosHiensFjP42oCq3/lsuncTMDw+GXdhuH9/37XeswBm7Y5uRJV1",
          "__VIEWSTATEGENERATOR": "8531ABAB",
          "__EVENTVALIDATION": "65POxR4Engbp9dK/YsnZS0SktNkwNiraqI1RN+uxJ0SrzzPFRW20SWCh7jmRHSA9GcMpHAk0DMslzXeuf8S8bzrHJ1vMvgOo3+TTqnUcYKSEp74I6GfZ6kMjIas2pctYKR6FXUxx3wtCudDhaYgTxAWj83mFgVq8UhPBcfUqZpUoOmoMh8K3V5JzEhOauBTJyG0tOiYnCP4YOkYeq8vfiB8oMRIT/L9OO0VH64uFiFZsKE6GPLNJxPnXcLz6kadO2M6BYg0vw8k7U/V8nzXOdA==",
          "ctl00$CntntPlcHldr$rbtACAD": "ACAD",
          "ctl00$CntntPlcHldr$ddlAcadClndr": i
     }
     html = (requests.post(url, data = payload)).text
     soup = BeautifulSoup(html, 'html.parser')
     table = soup.find(class_ = "table table-striped")
     table_rows = table.find_all("tr")

     for j in table_rows:
          elements = j.find_all('td')
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

                    for k in splitted_date:
                         if (year == k):
                              dates.append("".join("/" + k))
                         else:
                              dates.append(k)
                         date = "".join(dates)
                         if (date.find(year) != -1) or (date.find(next_year) != -1):
                              pass
                         else:
                              date = "".join(date + "/" + year)
                    terms.append(date + ", " + event)

     print(short_term, end="")
     print(" = ", end= "")
     print(terms)
