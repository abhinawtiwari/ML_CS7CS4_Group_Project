# IPL Score predictor
For ML Group project 
Members:
    Abhinaw Tiwari
    Asish Rath
    Vaibhav Srivastava

1) Recovered match links for each year of the chosen years from espncricinfo.com
    - issue faced: Links could not simply be recovered by visiting the website because the data on the page was dynamic. Links were included in cards that were generated dynamically and loaded upon user interaction (click event on IPL strip). Therefore, in order to load the cards that included the link, the strip had to be clicked first. Following that, urls were retrieved for every match.

2) Went to each match link to scrape ball by ball data
Issue faced: 
    - endless scrolling on dynamically loaded pages. In order to scroll the appropriate amount, we utilized Selenium to dynamically calculate the amount of down and up scroll based on page height.
    - The estimation of the scroll height was hampered by the pages' dynamic ads. Therefore, monitoring was required to ensure that the scraping was being done correctly.
    - After studying the html and css layout of the webpage, we thought that we could get the runs scored per ball data from the tag class='ds-leading-none ds-mb-0.5' but few balls had no commentary for them, hence the tag was different for them. This led to empty string being fetched for these tags and code breaking. To solve this we took the parent tag for such class. 
    - The problem faced with taking parent tag i.e.ds-ml-4 lg:ds-ml-3 was that we had commentary data along with run data. For this we just split the string on newline and took the first element.
    - scrolled up by a certain number of pixels when hitting page bottom. This number had to varied and checked to get a right number. But that didn't work for some cases because of variable height of the ads container at the bottom of the page. Then, scrolled up by a number of pixels equal to the height of the ad container. There were issue with this method also, for ads that came in right side cards of the page.
    
3) Trained model