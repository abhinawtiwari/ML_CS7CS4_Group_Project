file1 = open('url_extraction/2019_links.txt', 'r')
Lines = file1.readlines()
  
count = 0
list = []
# Strips the newline character
for line in Lines:
    count += 1
    # print("Line{}: {}".format(count, line.strip()))
    list.append(line)
print(list)