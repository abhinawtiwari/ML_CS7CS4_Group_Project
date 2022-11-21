import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from urllib.parse import urljoin
import csv

driver = webdriver.Chrome('/Users/aokiji/Downloads/chromedriver')
headers =["ball_no","run","is_wide","is_noBall","Wicket","is_legBye","isBye"]
f = open("ipl.csv","w")
writer = csv.writer(f)
writer.writerow(headers)

urls = ["https://www.espncricinfo.com/series/ipl-2020-21-1210595/kolkata-knight-riders-vs-mumbai-indians-5th-match-1216508/ball-by-ball-commentary", "https://www.espncricinfo.com/series/ipl-2020-21-1210595/sunrisers-hyderabad-vs-royal-challengers-bangalore-3rd-match-1216534/ball-by-ball-commentary"]
for url in urls:
    driver.get(url)

    #driver.get("https://www.espncricinfo.com/series/ipl-2020-21-1210595/sunrisers-hyderabad-vs-royal-challengers-bangalore-3rd-match-1216534/ball-by-ball-commentary")
    #driver1.get("https://www.espncricinfo.com/series/ipl-2020-21-1210595/mumbai-indians-vs-chennai-super-kings-1st-match-1216492/ball-by-ball-commentary/")
    # driver.implicitly_wait(10)
    # driver.find_element(By.ID,"onetrust-accept-btn-handler").click()

    print("Whats up")

    scroll_pause_time = 2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    for count in range(0,20):
        print("COUNTTT", count)
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            print("Inside break")
            driver.execute_script("window.scrollTo(0, -200)")  



    def extract_run_from_string(runs):
        run = ""


    ball_count = 1
    runs_list = []
    balls_list=[]
    runs_elements = driver.find_elements(By.XPATH,"//div[@class='ds-leading-none ds-mb-0.5']")
    ball_elements = driver.find_elements(By.XPATH,"//span[@class='ds-text-tight-s ds-font-regular ds-mb-1 lg:ds-mb-0 lg:ds-mr-3 ds-block ds-text-center']")
    for runs in runs_elements:
        print("Ball count", ball_count)
        runs_list.append(runs.text)

    for ball in ball_elements:
        balls_list.append(ball.text)

    final_run_list = runs_list[::-1]
    final_ball_list = balls_list[::-1]

    print(final_run_list)
    print(final_ball_list)


    def extract_run(runs):
        wicket = 0
        wide = 0
        no_ball = 0
        leg_bye = 0
        bye = 0
        if '(no ball) FOUR' in runs:
            run = 5
            no_ball = 1
        elif '(no ball) 1' in runs:
            run = 2
            no_ball = 1
        elif '(no ball) 2' in runs:
            run = 3
            no_ball = 1
        elif '(no ball) 3' in runs:
            run = 4
            no_ball = 1
        elif '(no ball) SIX' in runs:
            run = 7
            no_ball = 1
        elif '(no ball)' in runs:
            run = 1
            no_ball = 1
        elif '1 leg bye' in runs:
            run = 1
            leg_bye = 1
        elif '2 leg bye' in runs:
            run = 2
            leg_bye = 1
        elif '3 leg bye' in runs:
            run = 3
            leg_bye = 1
        elif '4 leg bye' in runs:
            run = 4
            leg_bye = 1
        elif '4 byes' in runs:
            run = 4 
            bye = 1
        elif '3 byes' in runs:
            run = 3 
            bye = 1
        elif '2 byes' in runs:
            run = 2 
            bye = 1
        elif '1 byes' in runs:
            run = 1 
            bye = 1

        elif '1 wide' in runs:
            run = 1
            wide = 1
        elif '2 wide' in runs:
            run = 2
            wide = 1
        elif '3 wide' in runs:
            run = 3
            wide = 1
        elif '4 wide' in runs:
            run = 4
            wide = 1
        elif '5 wide' in runs:
            run = 5
            wide = 1

        elif '1' in runs:
            run = 1

        elif '2' in runs:
            run = 2
        elif '3' in runs:
            run = 3
        elif 'FOUR' in runs:
            run = 4
        elif '5' in runs:
            run = 5
        elif 'SIX' in runs:
            run = 6
        elif 'no run' in runs:
            run = 0
        elif 'OUT' in runs:
            wicket = 1
            run = 0

        return run, wide, no_ball, wicket, leg_bye, bye



    total = 0
    
    for ball in range (len(final_ball_list)):
        run, wide, no_ball, wicket,leg_bye, bye = extract_run(final_run_list[ball])
        total +=run
        print(final_ball_list[ball]," ", run, " ",wide, " ", no_ball, " ", wicket," ",leg_bye," ",bye)
        writer.writerow([final_ball_list[ball],run,wide,no_ball,wicket,leg_bye,bye])

    print("Total", total)

f.close()


    
