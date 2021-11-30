# Creating lists for file path
first_file = ["CURRENT", "PAST"]
years = ["2021", "2020", "2019"]
second_file = ["ACADEMIC", "PREP"]
terms = ["10","20","30"]

# Gitting the range of the lists
range_length_first_file = range(len(first_file))
range_length_year = range(len(years))
range_length_second_file = range(len(second_file))
range_length_term = range(len(terms))

# The bool statement for the gaps
gap_line = False

for f in range_length_first_file:
     new_first_file = first_file[f]
     for y in range_length_year:
          new_year = years[y]
          for s in range_length_second_file:
               new_second_file = second_file[s]
               if (new_first_file == "CURRENT" and new_year != "2021"):
                    continue
               elif (new_first_file == "PAST" and new_year == "2021"):
                    continue
               else:
                    for t in range_length_term:
                         new_term = terms[t]
                         if (new_second_file == "PREP" and new_term == "30"):
                              continue
                         else:
                              # Openning and reading the file
                              open_read_file = (open(new_first_file + "/" + new_second_file + "/" + new_year + new_term + ".html")).read()

                              # Bringing the whole table
                              table = open_read_file.replace('\t\t\t<th scope="col" style="color:White;background-color:#007D40;">WEEK DAY</th><th scope="col" style="color:White;background-color:#007D40;">HIJRI DATE</th><th scope="col" style="color:White;background-color:#007D40;">GREGORIAN DATE</th><th scope="col" style="color:White;background-color:#007D40;">EVENTS</th>\n\t\t</tr><tr>', "$$$").replace('\t\t\t<th scope="col" style="color:White;background-color:#007D40;">DAY</th><th scope="col" style="color:White;background-color:#007D40;">WEEK</th><th scope="col" style="color:White;background-color:#007D40;">HIJRI DATE</th><th scope="col" style="color:White;background-color:#007D40;">GREGORIAN DATE</th><th scope="col" style="color:White;background-color:#007D40;">EVENTS</th>\n\t\t</tr><tr>', "$$$").replace("</table>", "$$$").split("$$$")

                              # Counting elements and gitting the needed area
                              length_table = len(table) - 1
                              range_table = range(2, length_table)

                              # Checking the gap bool statement
                              if (gap_line == False):
                                   gap_line = True
                              else:
                                   print("\n", end= "")

                              # Printing the second path with year
                              print(new_second_file + ", " + new_year + new_term)
                              half = False

                              for i in range_table:
                                   # Getting the table
                                   new_table = table[i]

                                   # Creating bool statements for starting and ending
                                   start = False
                                   end = False

                                   # Splitting each line for table
                                   splitted_lines = new_table.replace("\t", "").replace("<tbody><tr>", "").split("</tr><tr>")
                                   length_splitted_lines = len(splitted_lines)
                                   range_splitted_lines = range(length_splitted_lines)

                                   # Getting each splitted line
                                   for j in range_splitted_lines:
                                        splitted_items = splitted_lines[j].replace("<a>", "$$$").replace("</td>", "$$$").replace('">', "$$$").replace("</a>", "$$$").replace("\n", "").split("$$$")
                                        length_splitted = len(splitted_items)

                                        # Creating variable for date and event
                                        if (length_splitted == 11):
                                             date_item = splitted_items[5]
                                             event_item = splitted_items[8]
                                        elif (length_splitted == 13):
                                             date_item = splitted_items[7]
                                             event_item = splitted_items[10]

                                        if new_second_file == "PREP":
                                             if half == False:
                                                  print("\tFIRST HALF")
                                                  half += 1
                                             elif half == 1 and length_splitted_lines == 1:
                                                  print("\tSECOND HALF")
                                                  half += 1

                                        if (length_splitted == 11 and end == False):
                                             if start == False:
                                                  if (event_item.find("Classes begin") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                       start = True
                                             elif start == True:
                                                  if (event_item.find("Last day before") != -1):
                                                       continue
                                                  if (event_item.find("Holiday") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("resume") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("Break") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("Normal") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("Last day of classes") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                       end = True

                                        elif (length_splitted == 13 and end == False):
                                             if start == False:
                                                  if (event_item.find("Classes begin") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                       start = True
                                             elif start == True:
                                                  if (event_item.find("Last day before") != -1):
                                                       continue
                                                  if (event_item.find("Holiday") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("Break") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("resume") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("Normal") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                  elif (event_item.find("Last day of classes") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       else:
                                                            pass
                                                       print("\t" + date_item + ", " + event_item)
                                                       end = True