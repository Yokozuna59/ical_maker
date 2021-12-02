# Importing Mudules
import os

# Gitting files in directory
first_directory = os.listdir()
# The bool statement for the gaps
gap_line = False

for f in range(len(first_directory)):
     if (first_directory[f].find(".") != -1):
          pass
     else:
          second_directory = os.listdir(first_directory[f])
          for s in range(len(second_directory)):
               if (second_directory[s].find(".") != -1):
                    pass
               else:
                    third_directory = os.listdir(first_directory[f] + "/" + second_directory[s])
                    for t in range(len(third_directory)):
                         if (third_directory[t].find(".") != -1):
                              new_first_directory = first_directory[f]
                              new_second_directory = second_directory[s]
                              new_third_directory = third_directory[t]

                              print(new_first_directory + "/" + new_second_directory + "/" + new_third_directory)

                              open_read_file = (open(new_first_directory + "/" + new_second_directory + "/" + new_third_directory)).read()

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
                              print(new_second_directory + ", " + new_third_directory.replace(".html", ""))
                              half = False

                              for i in range_table:
                                   # Getting the table
                                   new_table = table[i]

                                   # Creating bool statements for starting and ending
                                   start = False
                                   end = False
                                   first_line = False
                                   year_change = False

                                   # Splitting each line for table
                                   splitted_lines = new_table.replace("\t", "").replace("<tbody><tr>", "").split("</tr><tr>")
                                   length_splitted_lines = len(splitted_lines)
                                   range_splitted_lines = range(length_splitted_lines)

                                   # Getting each splitted line
                                   for j in range_splitted_lines:
                                        splitted_items = splitted_lines[j].replace("amp;", "").replace("<a>", "$$$").replace("</td>", "$$$").replace('">', "$$$").replace("</a>", "$$$").replace("\n", "").split("$$$")
                                        length_splitted = len(splitted_items)

                                        if new_second_directory == "PREP":
                                             if half == False:
                                                  print("\tFIRST HALF")
                                                  half += 1
                                             elif half == 1 and length_splitted_lines == 1:
                                                  print("\tSECOND HALF")
                                                  half += 1

                                        if (((length_splitted == 11) or (length_splitted == 13)) and end == False):
                                             if (length_splitted == 11):
                                                  date_item = " ".join(splitted_items[5].replace("Sepember", "September").replace("January", "Jan").replace("February", "Feb").replace("March", "Mar").replace("April", "Apr").replace("June", "Jun").replace("July", "Jul").replace("August", "Aug").replace("September", "Sep").replace("October", "Oct").replace("November", "Nov").replace("December", "Dec").replace("Jan", "/1").replace("Feb", "/2").replace("Mar", "/3").replace("Apr", "/4").replace("May", "/5").replace("Jun", "/6").replace("Jul", "/7").replace("Aug", "/8").replace("Sep", "/9").replace("Oct", "/10").replace("Nov", "/11").replace("Dec", "/12").split())
                                                  event_item = " ".join(splitted_items[8].split())
                                             elif (length_splitted == 13):
                                                  date_item = " ".join(splitted_items[7].replace("Sepember", "September").replace("January", "Jan").replace("February", "Feb").replace("March", "Mar").replace("April", "Apr").replace("June", "Jun").replace("July", "Jul").replace("August", "Aug").replace("September", "Sep").replace("October", "Oct").replace("November", "Nov").replace("December", "Dec").replace("Jan", "/1").replace("Feb", "/2").replace("Mar", "/3").replace("Apr", "/4").replace("May", "/5").replace("Jun", "/6").replace("Jul", "/7").replace("Aug", "/8").replace("Sep", "/9").replace("Oct", "/10").replace("Nov", "/11").replace("Dec", "/12").split())
                                                  event_item = " ".join(splitted_items[10].split())
                                             splitted_date = date_item.replace("-", " ").split()
                                             if start == False:
                                                  if (first_line == False):
                                                       splitted_date = date_item.replace("-", " ").split()
                                                       year = splitted_date[len(splitted_date) - 1]
                                                       next_year = int(year) + 1
                                                       first_line = True
                                                  if (event_item.find("Classes begin") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       print("\t", end= "")
                                                       for x in range(len(splitted_date)):
                                                            if (year == splitted_date[x]):
                                                                 print("/", end= "")
                                                            print(splitted_date[x], end= "")

                                                       if ((date_item.find(str(year)) != -1) or (date_item.find(str(next_year)) != -1)):
                                                            pass
                                                       else:
                                                            print("/" + year, end= "")
                                                       print(", " + event_item)
                                                       start = True

                                             elif start == True:
                                                  if (year_change == False and (date_item.find(str(next_year)) != -1)):
                                                       year = str(next_year)
                                                       year_change = True
                                                  if (event_item.find("Last day before") != -1):
                                                       continue
                                                  if ((event_item.find("Holiday") != -1) or (event_item.find("resume") != -1) or (event_item.find("Break") != -1) or (event_item.find("Normal") != -1)):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       print("\t", end= "")
                                                       for x in range(len(splitted_date)):
                                                            if (year == splitted_date[x]):
                                                                 print("/", end= "")
                                                            print(splitted_date[x], end= "")

                                                       if ((date_item.find(str(year)) != -1) or (date_item.find(str(next_year)) != -1)):
                                                            pass
                                                       else:
                                                            print("/" + year, end= "")
                                                       print(", " + event_item)
                                                  elif (event_item.find("Last day of classes") != -1):
                                                       if (half == 1 or half == 2):
                                                            print("\t", end= "")
                                                       print("\t", end= "")
                                                       for x in range(len(splitted_date)):
                                                            if (year == splitted_date[x]):
                                                                 print("/", end= "")
                                                            print(splitted_date[x], end= "")

                                                       if ((date_item.find(str(year)) != -1) or (date_item.find(str(next_year)) != -1)):
                                                            pass
                                                       else:
                                                            print("/" + year, end= "")
                                                       print(", " + event_item)
                                                       end = True