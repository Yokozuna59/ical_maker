# Open and Read the file
from os import X_OK


html_page = (open("202120_CACAD_PREP.html")).read()

# Gitting the area were the table is
table = html_page.replace('<table class="table table-striped" cellspacing="0" rules="all" border="1" id="CntntPlcHldr_grdAcadClndr" style="border-collapse:collapse;">', "$$$").replace("</table>", "$$$").split("$$$")
if (len(table) == 5):
     ran = 4
     x = True
elif (len(table)):
     ran = 3
     x = False

# Splitting each line
for n in range(2, ran):
     table_e = table[n]
     lines = table_e.split("</tr><tr>")
     for i in range(len(lines)):
          splitted = lines[i].replace("<a>", "$$$").replace("</td>", "$$$").replace('">', "$$$").replace("</a>", "$$$").split("$$$")
          leng = len(splitted)
          rang = range(leng)
          for j in rang:
               if (leng == 13):
                    if (j == 7 or j == 10):
                         print(splitted[j])
               else:
                    if x == False:
                         if (j == 5 or j == 8):
                              if x == True:
                                   x = False
                              elif x == False:
                                   print(splitted[j])
                    else:
                         if (j == 5 or j == 8):
                              print(splitted[j])