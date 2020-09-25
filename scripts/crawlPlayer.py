import pandas as pd
import time
import pickle
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv 

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def getPlayer():
    with open('PL_data.csv', mode='r') as infile:
    	reader = csv.reader(infile)
	for rows in reader:
	   print(rows[0])
def getPlayerStats():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # connect webdriver
    url = "https://www.fifaindex.com/players/1/?league=13&order=desc"
    driver.get(url)

    # wait for gettig data
    time.sleep(3)
    count = 1
    # click event for gettig data
    relevant_features = ['Name','Ball Skills','Defence','Mental','Passing','Physical','Shooting','Goalkeeper','Traits']
    #print relevant_features[0]
    while True:
        players = driver.find_elements_by_css_selector("a.link-player")
        #print len(players)
        flag = 0
        footballers = dict()
        for player in players:
                if not player.text:
                    continue
                match_url =  player.get_attribute("href")
                man = player.text
                driver.execute_script("window.open('"+match_url+"', 'new_window')")
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[-1])
                elements = driver.find_elements_by_css_selector(".card.mb-5")
                #man = str(player.text)
                print len(elements)        
                footballers[man] = {}
                nm = 0;
		footballers[man]['Name'] = list()
		footballers[man]['Name'].append(man)
                footballers[man]['Traits']=list()
                for element in elements:
                    card_name = element.find_elements_by_css_selector(".card-header")[0].text
                    print card_name,nm
                    nm = nm+1
                    if card_name not in relevant_features:
                        continue
		    card_name = card_name
		    if card_name not in ['Traits']:
                    	footballers[man][card_name] = list()
                    card_values = element.find_elements_by_xpath(".//div[@class='card-body']/p")
 
                    for values in card_values:
                        temp =  str(values.text).split('\n')
			#temp[0] = temp[0].encode('utf-8', 'ignore').decode('utf-8')
                        if len(temp)==1:
                            footballers[man]['Traits'].append(temp[0])
                        else:
			    #temp[1] = temp[1].encode('utf-8', 'ignore').decode('utf-8')
                            footballers[man][card_name].append(temp[1])
                #print footballers[man]["Defence"]["Marking"]
                #print len(footballers[man])
                csv_file = "PL_Fifa_Data.csv"
		#footballers[man] = convert(footballers[man])
		#df = pd.DataFrame(footballers
		#df.to_csv(csv_file)
		'''
		try:
		    with open(csv_file, 'a') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=relevant_features)
			#writer.writeheader()
			writer.writerow([unicode(s).encode("utf-8") for s in footballers[man]])
		except IOError:
		    print("I/O error")
		'''
                with open(csv_file, 'a') as f:
                        w = csv.DictWriter(f, relevant_features)
                        w.writerow(footballers[man])
		
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                #driver.execute_script("window.history.go(-1)")
        count = count+1
        url = "https://www.fifaindex.com/players/"+str(count)+"/?league=13&order=desc"
        driver.get(url)
        time.sleep(3)
    driver.close()
