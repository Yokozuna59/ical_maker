import time
from selenium import webdriver #
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup #

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://registrar.kfupm.edu.sa/PastAcadYear")

select = Select(driver.find_element_by_id('CntntPlcHldr_ddlAcadClndr'))
time.sleep(2)
#select.select_by_value('202110')
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
tt = soup.find_all('option')
for i in tt:
     if (i.find('value="0"') != -1):
          pass
     else:
          print(i["value"])

"""
<option value="0">Select Calendar</option>
<option selected="selected" value="202110">Academic Calendar 2021-2022 (1443H): First Semester (211)</option>
<option value="202120">Academic Calendar 2021-2022 (1443H): Second Semester (212)</option>
<option value="202130">Academic Calendar 2021-2022 (1443H) : Summer Session (213)</option>
</select>
"""

     # driver.execute_script("window.open('https://registrar.kfupm.edu.sa/PastAcadYear', 'new_window')")

#open tab
     # new = driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')