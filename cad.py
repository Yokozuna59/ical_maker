# Importing libraries
from os import close

# Open and Read the file
html_page = open("202110_CACAD.html", "r")
read_page = html_page.read()

# Gitting the table
table = read_page.replace('\t\t\t<th scope="col" style="color:White;background-color:#007D40;">DAY</th><th scope="col" style="color:White;background-color:#007D40;">WEEK</th><th scope="col" style="color:White;background-color:#007D40;">HIJRI DATE</th><th scope="col" style="color:White;background-color:#007D40;">GREGORIAN DATE</th><th scope="col" style="color:White;background-color:#007D40;">EVENTS</th>\n\t\t</tr><tr>', "$$$").replace("</table>", "$$$").split("$$$")

# Counting elements
length_table = len(table)
if (length_table == 4):
     range_table = 3
     bool = False
elif (length_table == 6):
     range_table = 5
     bool = True

for n in range(2, range_table):
     # Getting item
     table_item = table[n]

     # Splitting each line
     splitted_lines = table_item.replace("\t", "").replace("<tbody><tr>", "").split("</tr><tr>")

     # Getting each splitted line
     for i in range(len(splitted_lines)):
          splitted = splitted_lines[i].replace("<a>", "$$$").replace("</td>", "$$$").replace('">', "$$$").replace("</a>", "$$$").split("$$$")
          length_splitted = len(splitted)
          range_splitted = range(length_splitted)
          for j in range_splitted:
               if (length_splitted == 13):
                    if (j == 7 or j == 10):
                         print(splitted[j])
               else:
                    if bool == False:
                         if (j == 5 or j == 8):
                              if bool == True:
                                   bool = False
                              elif bool == False:
                                   print(splitted[j])
                    else:
                         if (j == 5 or j == 8):
                              if (splitted[j] == '\n\n'):
                                   continue
                              else:
                                   print(splitted[j])
html_page.close()