import csv

file = open('scraped_data/2022_iplScore.csv')

type(file)
csvreader = csv.reader(file)
header = []
header = next(csvreader)
print(header)

res_dict = {}
rows = []
# match_ids_set = set()
for row in csvreader:
    rows.append(row)
    # print(row[0])
    match_id = row[0]
    res_dict[match_id] = row
    # match_ids_set.add(row[0])
# print(rows)

# for key, value in res_dict.items():
#     print(key, value)

# print(list(res_dict.values()))
file.close()

list_test_rows = list(res_dict.values())
print(list_test_rows)
  
with open('test_data.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(header)
    write.writerows(list_test_rows)