# importing modules
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select

# ignoring elements error
warnings.filterwarnings("ignore", category=DeprecationWarning)

years = ["https://registrar.kfupm.edu.sa/CurrentAcadYear"]#, "https://registrar.kfupm.edu.sa/PastAcadYear"]
prep = ['', 'Prep']

driver = webdriver.Chrome()
driver.maximize_window()
gap_line = False
aca = False

for i in years:
     driver.get(i)
     html = driver.page_source
     soup = BeautifulSoup(html, 'html.parser')

     for j in (0, 0):
          if aca == False:
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
                    options = Select(driver.find_element_by_id('CntntPlcHldr_ddlAcadClndr'))# + prep[j]))
                    options.select_by_value(choices[k]['value'])
                    print("\t" + choices[k]['value'])
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find(class_="table table-striped")
                    table_rows = table.find_all("tr")

                    for h in table_rows:
                         elements = h.find_all('td')
                         if (len(elements) != 0):
                              date = elements[3].text
                              event = elements[4].text

                              if (event.find("Last day before") != -1):
                                   continue
                              elif ((event.find("Classes begin") != -1) or(event.find("Holiday") != -1) or (event.find("resume") != -1) or (event.find("Break") != -1) or (event.find("Normal") != -1) or (event.find("Last day of classes") != -1)):
                                   print("\t\t" + date + ", " + event)
               aca = True

driver.close()

# webDriver(years)