import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from urllib.parse import urljoin
import csv

year = "2020"
team_name_dict = {
    "CSK":"Chennai Super Kings",
    "DC":"Delhi Capitals",
    "GT":"Gujarat Titans",
    "KKR":"Kolkate Night Riders",
    "LSG":"Lucknow Super Giants",
    "MI":"Mumbai Indians",
    "KXIP":"Kings XI Punjab",
    "RR":"Rajasthan Royals",
    "RCB":"Royal Challengers Bangalore",
    "SRH":"Sunrisers Hyderabad",
    "PBKS":"Punjab Kings"
}

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



def scroll_page_to_get_data(driver, idx, url):
    driver.get(url)
    
    driver.implicitly_wait(5)
    if(idx == 0):
        driver.find_element(By.ID,"onetrust-accept-btn-handler").click()
        driver.implicitly_wait(5)
    driver.find_element(By.XPATH,"//span[contains(text(), 'Commentary')]").click()
    
    scroll_pause_time = 3 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    for count in range(0,20):
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=0.7*i))  
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
    runs_elements = driver.find_elements(By.XPATH,"//div[@class='ds-ml-4 lg:ds-ml-3']")
    return runs_elements

def scrape_balls_of_innings(driver):
    balls_elements = driver.find_elements(By.XPATH,"//span[@class='ds-text-tight-s ds-font-regular ds-mb-1 lg:ds-mb-0 lg:ds-mr-3 ds-block ds-text-center']")
    return balls_elements

def get_venue_played(driver):
    venue_name_string = driver.find_element(By.XPATH,"//div[@class='ds-text-tight-m ds-font-regular ds-text-ui-typo-mid']")
    venue_name_obj = venue_name_string.text
    print("What is venue name obj", venue_name_obj)
    venue_name = venue_name_obj.split(',')[1]
    print("What is venue name", venue_name)
    return venue_name

def get_team_name(driver):
    team_name = driver.find_element(By.XPATH,"//span[@class='ds-text-tight-s ds-font-regular ds-text-ui-typo']")
    print("What is the team name", team_name.text)
    if team_name.text in team_name_dict.keys():
        return team_name_dict[team_name.text]
    return ''


def get_list_of_runs(runs_elems):
    runs_list = []
    for runs in runs_elems:
        run_text = runs.text
        final_run_str = run_text.split('\n')[0]
        runs_list.append(final_run_str)
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


def prepare_csv(writer, match_id, team_name, venue_name, final_ball_list,final_run_list):
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
        write_to_csv(writer,[year+"_"+str(match_id),team_name,venue_name,final_ball_list[ball],run,wide,no_ball,wicket,leg_bye,bye,total])

    print("Total", total)

def prepareUrlsToScrape():
    file1 = open('url_extraction/test_links.txt', 'r')
    Lines = file1.readlines()
    
    list = []
    for line in Lines:
        list.append(line)
    print(list)
    return list

def main():
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()

    headers =["match_id","team_name","venue_name","ball_no","run","is_wide","is_noBall","Wicket","is_legBye","isBye","totalScore"]
    f = open("iplScore.csv","w")
    writer = csv.writer(f)
    writer.writerow(headers)

    urls = prepareUrlsToScrape()
    match_id = 1

    for idx, url in enumerate(urls):
        print('starting scraping for url ', url)
        print("THIS IS MATCH NUMBER")
        print("--------------------------------")
        print(match_id)
        driver_obj = scroll_page_to_get_data(driver, idx, url)
        team_name = get_team_name(driver_obj)
        venue_name = get_venue_played(driver_obj)
        run_data = scrape_runs_per_ball_data(driver_obj)
        ball_data = scrape_balls_of_innings(driver_obj)
        runs_list = get_list_of_runs(run_data)
        balls_list = get_list_of_balls(ball_data)
        prepare_csv(writer,match_id,team_name, venue_name, balls_list,runs_list)
        match_id+=1

    f.close()

if __name__ == "__main__":
    main()



    
