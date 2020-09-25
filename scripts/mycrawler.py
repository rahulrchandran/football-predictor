import pandas as pd
import time
import csv
import pickle
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def getRatings():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # connect webdriver
    url = "https://1xbet.whoscored.com/Regions/252/Tournaments/2/England-Premier-League"
    driver.get(url)

    # wait for gettig data
    time.sleep(3)

    # click event for gettig data
    driver.find_elements_by_css_selector(".qc-cmp-button")[1].click()

    # wait for gettig data
    time.sleep(3)

    while True:
	
        matches = driver.find_elements_by_css_selector("a.result-1.rc")
        #away = driver.find_elements_by_css_selector("a.team-link")
        flag = 0
        i = 0
        for match in matches:
            try:
                match_url =  match.get_attribute("href")
		if "vs" in match.text:
                    raise WebDriverException
		home = driver.find_elements_by_css_selector("a.team-link")
		hometeam = home[i].text
                awayteam = home[i+1].text
		i = i+2
		print hometeam+" "+match.text+" "+awayteam
		players = []
                players.append(hometeam+" "+match.text+" "+awayteam)         
                #print driver.current_window_handle
                driver.execute_script("window.open('"+match_url+"', 'new_window')")
                #ActionChains(driver).key_down(Keys.CONTROL).click(match).key_up(Keys.CONTROL).perform()
                time.sleep(5)
                #print driver.window_handles
                driver.switch_to.window(driver.window_handles[-1])
                #print driver.current_window_handle
                #match.click()
                time.sleep(5)
                elements = driver.find_elements_by_css_selector(".player")
                #time.sleep(3);
        	
                
                #elements = driver.find_elements_by_css_selector(".player")
                #players = []
                for element in elements:
                    name = element.find_elements_by_css_selector(".player-name-wrapper")[0].get_attribute("title")
                    ratings = element.find_elements_by_css_selector(".player-stat-value")[0].text
		    player = []
                    if ratings:
                        player.append(name)
                        player.append(ratings)
                        players.append(player)
                driver.close()
                #print "This tab is done"
                driver.switch_to.window(driver.window_handles[0])
                #driver.execute_script("window.history.go(-1)")
		csv_file = "ratings_epl.csv"
		with open(csv_file, 'a') as f:
                        w = csv.writer(f)
                        w.writerow(players)
             
            except WebDriverException:
                print "Element is not clickable"
                flag = 1
                previous = driver.find_elements_by_css_selector(".previous.button.ui-state-default.rc-l.is-default")
                previous[0].click()
                time.sleep(5)
                break
        if flag == 0:
            driver.find_elements_by_css_selector(".previous.button.ui-state-default.rc-l.is-default")[0].click()
            time.sleep(5)
        #matches = driver.find_elements_by_css_selector(".result")
        #print previous.text   
    driver.close()
