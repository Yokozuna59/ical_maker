# Importing libraries
from os import close

first_file = ["CURRENT", "PAST"]
range_length_first_file = range(len(first_file))

year = ["2021", "2020", "2019"]
range_length_year = range(len(year))

second_file = ["ACADEMIC", "PREP"]
range_length_second_file = range(len(second_file))

term = ["10","20","30"]
range_length_term = range(len(term))

first_line = False

for f in range_length_first_file:
     new_first_file = first_file[f]
     for y in range_length_year:
          new_year = year[y]
          for s in range_length_second_file:
               new_second_file = second_file[s]
               if (new_first_file == "CURRENT" and new_year != "2021"):
                    continue
               elif (new_first_file == "PAST" and new_year == "2021"):
                    continue
               else:
                    for t in range_length_term:
                         new_term = term[t]
                         if (new_second_file == "PREP" and new_term == "30"):
                              continue
                         else:
                              open_read_page = (open(new_first_file + "/" + new_second_file + "/" + new_year + new_term + ".html")).read()

                              halfs = open_read_page.replace("FirstHalf", "").replace("SecondHalf", "").replace("</span></h3></center>", "&&&").replace('<center><h3><span id="CntntPlcHldr_lbl" style="color:#007D40;">', "&&&").split("&&&")
                              first_half = halfs[1]
                              print(first_half)
                              second_half = halfs[3]
                              print(second_half)

                              # Gitting the table
                              table = open_read_page.replace('\t\t\t<th scope="col" style="color:White;background-color:#007D40;">WEEK DAY</th><th scope="col" style="color:White;background-color:#007D40;">HIJRI DATE</th><th scope="col" style="color:White;background-color:#007D40;">GREGORIAN DATE</th><th scope="col" style="color:White;background-color:#007D40;">EVENTS</th>\n\t\t</tr><tr>', "$$$").replace('\t\t\t<th scope="col" style="color:White;background-color:#007D40;">DAY</th><th scope="col" style="color:White;background-color:#007D40;">WEEK</th><th scope="col" style="color:White;background-color:#007D40;">HIJRI DATE</th><th scope="col" style="color:White;background-color:#007D40;">GREGORIAN DATE</th><th scope="col" style="color:White;background-color:#007D40;">EVENTS</th>\n\t\t</tr><tr>', "$$$").replace("</table>", "$$$").split("$$$")

                              # Counting elements
                              length_table = len(table)
                              if (length_table == 4):
                                   range_table = 3
                              elif (length_table == 6):
                                   range_table = 5

                              if (first_line == False):
                                   print(new_second_file + ", " + new_year + new_term)
                                   first_line = True
                              else:
                                   print("\n" + new_second_file + ", " + new_year + new_term)
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
                                                  if new_second_file == "PREP":
                                                       if (j == 7):
                                                            print("\t\t" + splitted[j], end= "")
                                                       elif (j == 10):
                                                            print(", " + splitted[j])
                                                  else:
                                                       if (j == 7):
                                                            print("\t" + splitted[j], end= "")
                                                       elif (j == 10):
                                                            print(", " + splitted[j])
                                             elif (length_splitted == 11):
                                                  if new_second_file == "PREP":
                                                       if (j == 5):
                                                            print("\t\t" + splitted[j], end= "")
                                                       elif (j == 8):
                                                            print(", " + splitted[j])
                                                  else:
                                                       if (j == 5):
                                                            print("\t" + splitted[j], end= "")
                                                       elif (j == 8):
                                                            print(", " + splitted[j])