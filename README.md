# IPL Score predictor
For ML Group project 
Members:
    Abhinaw Tiwari
    Asish Rath
    Vaibhav Srivastava

Recovered match links for each year of the chosen years from espncricinfo.com
    - issue faced: Links could not simply be recovered by visiting the website because the data on the page was dynamic. Links were included in cards that were generated dynamically and loaded upon user interaction (click event on IPL strip). Therefore, in order to load the cards that included the link, the strip had to be clicked first. Following that, urls were retrieved for every match.

went to each match link to scrape ball by ball data
Issue faced: 
    - endless scrolling on dynamically loaded pages. In order to scroll the appropriate amount, we utilized Selenium to dynamically calculate the amount of down and up scroll based on page height.
    - The estimation of the scroll height was hampered by the pages' dynamic ads. Therefore, monitoring was required to ensure that the scraping was being done correctly.

trained model