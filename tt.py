from os import read
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup

text = pytesseract.image_to_string(r"port2.jpg")
text1 = text.replace("Sunday", "").replace("Monday", "").replace("Tuesday", "").replace("Wednesday", "").replace("Thursday","")


ttttt = (open("Weekly Schedule.html", mode='r', encoding='utf-8')).read()
tt1 = ttttt.replace(">&nbsp;</td>\n</tr>\n<tr>\n<th rowspan=","$$$").split("$$$")
print(tt1[5])
# .replace(">&nbsp;</td>", "").replace("<tr>", "").replace("</tr>", "").replace("dddefault", "")