# Importing libraries
from os import close, stat_result
from typing import ContextManager

first_file = ["CURRENT", "PAST"]
range_length_first_file = range(len(first_file))

year = ["2021", "2020", "2019"]
range_length_year = range(len(year))

second_file = ["ACADEMIC", "PREP"]
range_length_second_file = range(len(second_file))

term = ["10","20","30"]
range_length_term = range(len(term))

halfs = ["FIRST HALF", "SECOND HALF"]

gap_line = False

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

                              # Gitting the table
                              table = open_read_page.replace('\t\t\t<th scope="col" style="color:White;background-color:#007D40;">WEEK DAY</th><th scope="col" style="color:White;background-color:#007D40;">HIJRI DATE</th><th scope="col" style="color:White;background-color:#007D40;">GREGORIAN DATE</th><th scope="col" style="color:White;background-color:#007D40;">EVENTS</th>\n\t\t</tr><tr>', "$$$").replace('\t\t\t<th scope="col" style="color:White;background-color:#007D40;">DAY</th><th scope="col" style="color:White;background-color:#007D40;">WEEK</th><th scope="col" style="color:White;background-color:#007D40;">HIJRI DATE</th><th scope="col" style="color:White;background-color:#007D40;">GREGORIAN DATE</th><th scope="col" style="color:White;background-color:#007D40;">EVENTS</th>\n\t\t</tr><tr>', "$$$").replace("</table>", "$$$").split("$$$")

                              # Counting elements
                              length_table = len(table)
                              range_table = length_table - 1

                              if (gap_line == False):
                                   gap_line = True
                              else:
                                   print("\n", end= "")
                              print(new_second_file + ", " + new_year + new_term)
                              half = 0

                              for n in range(2, range_table):
                                   # Getting item
                                   table_item = table[n]
                                   start = False
                                   end = False

                                   # Splitting each line
                                   splitted_lines = table_item.replace("\t", "").replace("<tbody><tr>", "").split("</tr><tr>")
                                   length_splitted_lines = len(splitted_lines)

                                   # Getting each splitted line
                                   for i in range(length_splitted_lines):
                                        splitted = splitted_lines[i].replace("<a>", "$$$").replace("</td>", "$$$").replace('">', "$$$").replace("</a>", "$$$").replace("\n", "").split("$$$")
                                        length_splitted = len(splitted)
                                        range_splitted = range(length_splitted)

                                        if new_second_file == "PREP":
                                             if half == 0:
                                                  print("\t" + halfs[half])
                                                  half += 1
                                             elif half == 1 and length_splitted_lines == 1:
                                                  print("\t" + halfs[half])
                                                  half += 1

                                        if (length_splitted == 11 and end == False):
                                             if start == False:
                                                  if (splitted[8].find("Classes begin") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[5], end= "")
                                                       print(", " + splitted[8])
                                                       start = True
                                             elif start == True:
                                                  if (splitted[8].find("Holiday") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[5], end= "")
                                                       print(", " + splitted[8])
                                                  elif (splitted[8].find("Break") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[5], end= "")
                                                       print(", " + splitted[8])
                                                  elif (splitted[8].find("Last day of classes") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[5], end= "")
                                                       print(", " + splitted[8])
                                                       end = True

                                        elif (length_splitted == 13 and end == False):
                                             if start == False:
                                                  if (splitted[10].find("Classes begin") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[7], end= "")
                                                       print(", " + splitted[10])
                                                       start = True
                                             elif start == True:
                                                  if (splitted[10].find("Holiday") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[7], end= "")
                                                       print(", " + splitted[10])
                                                  elif (splitted[10].find("Break") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[7], end= "")
                                                       print(", " + splitted[10])
                                                  elif (splitted[10].find("Last day of classes") != -1):
                                                       if (half == 1):
                                                            print("\t", end= "")
                                                       elif (half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + splitted[7], end= "")
                                                       print(", " + splitted[10])
                                                       end = True