# Open and Read the file
html_page = (open("202110_CACAD_PREP.html")).read()

# Gitting the area were the table is
table = html_page.replace('<table class="table table-striped" cellspacing="0" rules="all" border="1" id="CntntPlcHldr_grdAcadClndr" style="border-collapse:collapse;">', "$$$").split("$$$")
table = table[1]

# Splitting each line
lines = table.split("</tr><tr>")

for i in range(len(lines)):
     splitted = lines[i].replace("<a>", "$$$").replace("</td>", "$$$").replace('">', "$$$").replace("</a>", "$$$").split("$$$")
     for j in range(len(splitted)):
          if (j == 7 or j== 10):
               print(splitted[j])