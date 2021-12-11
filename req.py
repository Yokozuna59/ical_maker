import requests
from bs4 import BeautifulSoup

# open the registrar current year page then scrap it
url = ("https://registrar.kfupm.edu.sa/CurrentAcadYear")
r = (requests.get(url)).text
soup = BeautifulSoup(r, 'html.parser')

reg_terms =[]
#.replace("-%s" %term, " " + str(term)).replace("-%s" %next_year, " " + str(next_year)).split())
rep = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "Sepember", "October", "November", "December", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "jul", "Aug", "Sep", "Oct", "Nov", "Dec",]
rep_to = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Sep", "Oct", "Nov", "Dec", "/1", "/2", "/3", "/4", "/5", "/6", "/7", "/8", "/9", "/10", "/11", "12"]

choices = soup.find_all('option')
for i in choices:
     if (i["value"].find("0") != 0):
          reg_terms.append(i["value"])

for i in reg_terms:
  term = i[2:5]
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
      date = " ".join(elements[3].text.split())
      event = " ".join(elements[4].text.split())
      terms.append(date + ", " + event)
  print(term, end="")
  print(" = ", end= "")
  print(terms)
  print("\n", end="")