from bs4 import BeautifulSoup

with open("htmls/2022.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

f = open("2022_links.txt", "w")

for span in soup.find_all('span', {'class' : 'match-no'}):
    links = span.find_all('a')
    for link in links:
        print(link['href'])
        f.write(link['href'])
        f.write("\n")

f.close()