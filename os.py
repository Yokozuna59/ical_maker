import os
first_directory = os.listdir()

for f in range(len(first_directory)):
     first_directory = os.listdir()
     if (first_directory[f].find(".") != -1):
          pass
     else:
          print(first_directory[f])
          second_directory = os.listdir(first_directory[f])
          for s in range(len(second_directory)):
               if (second_directory[s].find(".") != -1):
                    pass
               else:
                    print("\t" + second_directory[s])
                    third_directory = os.listdir(first_directory[f] + "/" + second_directory[s])
                    for t in range(len(third_directory)):
                         if (third_directory[t].find(".") != -1):
                              print("\t\t" + third_directory[t])