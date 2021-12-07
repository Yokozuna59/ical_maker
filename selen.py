# importing modules
import time
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select

# ignoring elements error
warnings.filterwarnings("ignore", category=DeprecationWarning)

driver = webdriver.Chrome()
driver.maximize_window()
gap_line = False

years = ['CurrentAcadYear']#, 'PastAcadYear']
prep = ['', 'Prep']
halfs = ['First Half', 'Second Half']

for i in years:
     driver.get('https://registrar.kfupm.edu.sa/' + i)
     html = driver.page_source
     soup = BeautifulSoup(html, 'html.parser')

     for j in (0, 1):
          driver.find_element_by_id('CntntPlcHldr_rbtACAD_' + str(j)).click()
          html = driver.page_source
          soup = BeautifulSoup(html, 'html.parser')

          if (gap_line == False):
               gap_line = True
          else:
               print("\n", end="")
          print((soup.find_all('h3')[0].text).replace(' :', ''))

          choices = soup.find_all('option')

          for k in range(1, len(choices)):
               options = Select(driver.find_element_by_id('CntntPlcHldr_ddlAcadClndr' + prep[j]))
               options.select_by_value(choices[k]['value'])
               print("\t" + choices[k]['value'])

               html = driver.page_source
               soup = BeautifulSoup(html, 'html.parser')

               if (j == 0):
                    table = soup.find(class_="table table-striped")
                    table_rows = table.find_all("tr")

                    for l in table_rows:
                         elements = l.find_all('td')
                         if (len(elements) != 0):
                              date = elements[3].text
                              event = elements[4].text

                              if (event.find("Last day before") != -1):
                                   continue
                              elif ((event.find("Classes begin") != -1) or(event.find("Holiday") != -1) or (event.find("resume") != -1) or (event.find("Break") != -1) or (event.find("Normal") != -1) or (event.find("Last day of classes") != -1)):
                                   print("\t\t" + date + ", " + event)
               else:
                    table = soup.find_all(class_="table table-striped")
                    for l in (0, 1):
                         print("\t\t" + halfs[l])

                         table_rows = table[l].find_all("tr")

                         for m in table_rows:
                              elements = m.find_all('td')
                              if (len(elements) != 0):
                                   date = elements[3].text
                                   event = elements[4].text

                                   if (event.find("Last day before") != -1):
                                        continue
                                   elif ((event.find("Classes begin") != -1) or(event.find("Holiday") != -1) or (event.find("resume") != -1) or (event.find("Break") != -1) or (event.find("Normal") != -1) or (event.find("Last day of classes") != -1)):
                                        print("\t\t\t" + date + ", " + event)
driver.close()