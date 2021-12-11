# importing modules
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select
import sys

sys.argv[2:]

# ignores the waring
warnings.filterwarnings("ignore", category = DeprecationWarning)

# open and minimize the browser
driver = webdriver.Chrome()
driver. maximize_window()

# the bool statement for gap line
gap_line = False

tab = ("\t")
prep = ["", "Prep"]
halfs = ["First Half", "Second Half"]


# open the registrar current year page then scrap it
driver.get("https://registrar.kfupm.edu.sa/CurrentAcadYear")
soup = BeautifulSoup(driver.page_source, 'html.parser')

for i in (0, 1):
     # click the radio button then scrap the page
     driver.find_element_by_id('CntntPlcHldr_rbtACAD_' + str(i)).click()
     html = driver.page_source
     soup = BeautifulSoup(html, 'html.parser')

     # check the gap_line statement
     if (gap_line == False):
          gap_line = True
     else:
          print("\n", end="")

     # print the panel heading
     print((soup.find_all('h3')[0].text).replace(' :', ''))

     # create variable "chioces" for the options in select
     choices = soup.find_all('option')

     for k in range(1, len(choices)):
          # choose the indext choice in the list of options
          options = Select(driver.find_element_by_id('CntntPlcHldr_ddlAcadClndr' + prep[i]))
          options.select_by_value(choices[k]['value'])

          # print the value == term
          term = choices[k]['value']
          next_year = int(term) + 1
          first_line = False
          print(tab + term)

          # scrap the current page
          html = driver.page_source
          soup = BeautifulSoup(html, 'html.parser')

          # if j == 0 then Academic
          if (i == 0):
               table = soup.find(class_="table table-striped")
               table_rows = table.find_all("tr")
               cont = False

               for l in table_rows:
                    elements = l.find_all('td')
                    if (len(elements) != 0):
                         date = " ".join(elements[3].text.replace("Sepember", "Sep").replace("January", "Jan").replace("February", "Feb").replace("March", "Mar").replace("April", "Apr").replace("June", "Jun").replace("July", "Jul").replace("August", "Aug").replace("September", "Sep").replace("October", "Oct").replace("November", "Nov").replace("December", "Dec").replace("Jan", "/1").replace("Feb", "/2").replace("Mar", "/3").replace("Apr", "/4").replace("May", "/5").replace("Jun", "/6").replace("Jul", "/7").replace("Aug", "/8").replace("Sep", "/9").replace("Oct", "/10").replace("Nov", "/11").replace("Dec", "/12").replace("-%s" %term, " " + str(term)).replace("-%s" %next_year, " " + str(next_year)).split())
                         event = elements[4].text

                         if (event.find("Last day before") != -1):
                              continue
                         elif ((event.find("Classes begin") != -1) or(event.find("Holiday") != -1) or (event.find("resume") != -1) or (event.find("Break") != -1) or (event.find("Normal") != -1) or (event.find("Last day of classes") != -1)):
                              cont = True

                         splitted_date = date.split()
                         if (first_line == False):
                              splitted_date = date.replace("-", " ").split()
                              year = splitted_date[len(splitted_date) - 1]
                              next_year = int(year) + 1
                              first_line = True

                         if (date.find(str(next_year)) != -1):
                              year = str(next_year)
                              year_change = True

                         if (cont == True):
                              print(tab*2, end="")
                              for n in range(len(splitted_date)):
                                   if (year == splitted_date[n]):
                                        print("/", end= "")
                                   print(splitted_date[n].replace("-/", "/"), end= "")

                              if ((date.find(str(year)) != -1) or (date.find(str(next_year)) != -1)):
                                   pass
                              else:
                                   print("/" + year, end= "")
                              print(", " + event)
                              cont = False

          # if j == 1 the Prep
          else:
               cont = False
               table = soup.find_all(class_="table table-striped")
               for l in (0, 1):
                    print(tab*2 + halfs[l])

                    table_rows = table[l].find_all("tr")

                    for m in table_rows:
                         elements = m.find_all('td')
                         if (len(elements) != 0):
                              date = " ".join(elements[3].text.replace("Sepember", "Sep").replace("January", "Jan").replace("February", "Feb").replace("March", "Mar").replace("April", "Apr").replace("June", "Jun").replace("July", "Jul").replace("August", "Aug").replace("September", "Sep").replace("October", "Oct").replace("November", "Nov").replace("December", "Dec").replace("Jan", "/1").replace("Feb", "/2").replace("Mar", "/3").replace("Apr", "/4").replace("May", "/5").replace("Jun", "/6").replace("Jul", "/7").replace("Aug", "/8").replace("Sep", "/9").replace("Oct", "/10").replace("Nov", "/11").replace("Dec", "/12").replace("-%s" %term, " " + str(term)).replace("-%s" %next_year, " " + str(next_year)).split())
                              event = elements[4].text

                              if (event.find("Last day before") != -1):
                                   continue
                              elif ((event.find("Classes begin") != -1) or(event.find("Holiday") != -1) or (event.find("resume") != -1) or (event.find("Break") != -1) or (event.find("Normal") != -1) or (event.find("Last day of classes") != -1)):
                                   cont = True

                              splitted_date = date.split()
                              if (first_line == False):
                                   splitted_date = date.replace("-", " ").split()
                                   year = splitted_date[len(splitted_date) - 1]
                                   next_year = int(year) + 1
                                   first_line = True

                              if (date.find(str(next_year)) != -1):
                                   year = str(next_year)
                                   year_change = True

                              if (cont == True):
                                   print(tab*3, end="")
                                   for n in range(len(splitted_date)):
                                        if (year == splitted_date[n]):
                                             print("/", end= "")
                                        print(splitted_date[n].replace("-/", "/"), end= "")

                                   if ((date.find(str(year)) != -1) or (date.find(str(next_year)) != -1)):
                                        pass
                                   else:
                                        print("/" + year, end= "")
                                   print(", " + event)
                                   cont = False

driver.close()