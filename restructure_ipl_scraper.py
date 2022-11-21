import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from urllib.parse import urljoin
import csv



def write_to_csv(writer, data):
    writer.writerow(data)

def is_wide(ball_data):
    if "wide" in ball_data:
        return 1
    return 0

def is_no_ball(ball_data):
    if '(no ball)' in ball_data:
        return 1
    return 0

def is_leg_bye(ball_data):
    if 'leg bye' in ball_data:
        return 1
    return 0

def is_bye(ball_data):
    if 'byes' in ball_data:
        return 1
    return 0

def is_wicket(ball_data):
    if 'OUT' in ball_data:
        return 1
    return 0



def scroll_page_to_get_data(driver, url):
    driver.get(url)
    scroll_pause_time = 3 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    for count in range(0,20):
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
    return driver


def scrape_runs_per_ball_data(driver):
    runs_elements = driver.find_elements(By.XPATH,"//div[@class='ds-leading-none ds-mb-0.5']")
    return runs_elements

def scrape_balls_of_innings(driver):
    balls_elements = driver.find_elements(By.XPATH,"//span[@class='ds-text-tight-s ds-font-regular ds-mb-1 lg:ds-mb-0 lg:ds-mr-3 ds-block ds-text-center']")
    return balls_elements

def get_list_of_runs(runs_elems):
    runs_list = []
    for runs in runs_elems:
        runs_list.append(runs.text)
    return runs_list[::-1]

def get_list_of_balls(ball_elems):
    balls_list = []
    for ball in ball_elems:
        balls_list.append(ball.text)
    return balls_list[::-1]


def extract_run(runs):
    if '(no ball) FOUR' in runs:
        run = 5
    elif '(no ball) 1' in runs:
        run = 2
    elif '(no ball) 2' in runs:
        run = 3
    elif '(no ball) 3' in runs:
        run = 4
    elif '(no ball) SIX' in runs:
        run = 7
    elif '(no ball)' in runs:
        run = 1
    elif '1 leg bye' in runs:
        run = 1
    elif '2 leg bye' in runs:
        run = 2
    elif '3 leg bye' in runs:
        run = 3
    elif '4 leg bye' in runs:
        run = 4
    elif '4 byes' in runs:
        run = 4 
    elif '3 byes' in runs:
        run = 3 
    elif '2 byes' in runs:
        run = 2 
    elif '1 byes' in runs:
        run = 1 
    elif '1 wide' in runs:
        run = 1
    elif '2 wide' in runs:
        run = 2
    elif '3 wide' in runs:
        run = 3
    elif '4 wide' in runs:
        run = 4
    elif '5 wide' in runs:
        run = 5
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
        run = 0

    return run


def prepare_csv(writer,final_ball_list,final_run_list):
    total = 0
    
    for ball in range (len(final_ball_list)):
        run = extract_run(final_run_list[ball])
        wide = is_wide(final_run_list[ball])
        no_ball = is_no_ball(final_run_list[ball])
        wicket = is_wicket(final_run_list[ball])
        leg_bye = is_leg_bye(final_run_list[ball])
        bye = is_bye(final_run_list[ball])
        total +=run
        print(final_ball_list[ball]," ", run, " ",wide, " ", no_ball, " ", wicket," ",leg_bye," ",bye,"",total)
        write_to_csv(writer,[final_ball_list[ball],run,wide,no_ball,wicket,leg_bye,bye,total])

    print("Total", total)


def main():
    driver = webdriver.Chrome('/Users/aokiji/Downloads/chromedriver')
    headers =["ball_no","run","is_wide","is_noBall","Wicket","is_legBye","isBye","totalScore"]
    f = open("iplScore.csv","w")
    writer = csv.writer(f)
    writer.writerow(headers)
    urls = ["https://www.espncricinfo.com/series/ipl-2020-21-1210595/kolkata-knight-riders-vs-mumbai-indians-5th-match-1216508/ball-by-ball-commentary", "https://www.espncricinfo.com/series/ipl-2020-21-1210595/sunrisers-hyderabad-vs-royal-challengers-bangalore-3rd-match-1216534/ball-by-ball-commentary","https://www.espncricinfo.com/series/ipl-2020-21-1210595/delhi-capitals-vs-kolkata-knight-riders-16th-match-1216515/ball-by-ball-commentary"]
    for url in urls:
        driver_obj = scroll_page_to_get_data(driver, url)
        run_data = scrape_runs_per_ball_data(driver_obj)
        ball_data = scrape_balls_of_innings(driver_obj)
        runs_list = get_list_of_runs(run_data)
        balls_list = get_list_of_balls(ball_data)
        prepare_csv(writer,balls_list,runs_list)

    f.close()

if __name__ == "__main__":
    main()



    
