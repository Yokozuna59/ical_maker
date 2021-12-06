import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://registrar.kfupm.edu.sa/CurrentAcadYear")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
tt = soup.find_all('option')


for i in range(1, len(tt)):
     select = Select(driver.find_element_by_id('CntntPlcHldr_ddlAcadClndr'))
     select.select_by_value(tt[i]["value"])
     time.sleep(2)
     html = driver.page_source
     soup = BeautifulSoup(html, 'html.parser')
     table = soup.find(class_="table table-striped")
     table_rows = table.find_all("tr")

     for tr in table_rows:
          td = tr.find_all('td')
          if (len(td) != 0):
               for j in td:
                    if (td.find("Last day before") != -1):
                         continue
                    elif ((td.find("Classes begin") != -1) or(td.find("Holiday") != -1) or (td.find("resume") != -1) or (td.find("Break") != -1) or (td.find("Normal") != -1) or (td.find("Last day of classes") != -1)):
                         print(td[3].text, end= ", ")
                         print(td[4].text)
     print("\n\n\n\n\n")
     # string = str(table_rows).replace("[", "").replace("]", "")

     # soup = BeautifulSoup(string, 'html.parser')
     # for tr in event:
     #      td = event.find_all
     # event = soup.find_all("a")
driver.close()



     # driver.execute_script("window.open('https://registrar.kfupm.edu.sa/PastAcadYear', 'new_window')")

#open tab
     # new = driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')