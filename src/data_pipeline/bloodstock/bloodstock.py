import requests

from bs4 import BeautifulSoup

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import random
import decimal


def weatherby(browser, horse, df1, df2):
        
    search_form=browser.find_elements_by_xpath('//a[@class="ui-tabs__tab pp-tabs__tab hidden-xs-down hidden-sm-down"]')
    search_form[0].click()
        
    time.sleep(3)
        
    timeout = 10
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='hp-raceRecords__label']")))
        
    element2 = browser.find_elements_by_xpath("//td[@class='ui-table__cell']")
    titles = [x.text for x in element2]
    year_perf=titles[-36:]
    year_perf_2 = titles[-18:]
    top_rpr = titles[10]
    total_earnings = titles[7]
    total_starts=titles[1]

    age_element = browser.find_elements_by_xpath("//dt[@class='pp-definition__term']")
    age_element_info = [x.text for x in age_element]
    age=age_element_info[0]

    sire = browser.find_elements_by_xpath("//a[@class='ui-link ui-link_table js-popupLink hp-horseDefinition__link']")
    sire_info = [x.text for x in sire]

    stud = browser.find_elements_by_xpath("//span[@class='hp-nameRow__studFee__value']")
    stud_fee = [x.text for x in stud]
    
    comments = browser.find_elements_by_xpath("//dd[@class='pp-definition__description']")
    sire_comments = [x.text for x in comments]

    table_option1 = [age,
                    sire_info[0],
                    sire_info[1],
                    sire_info[2],
                    stud_fee[0],
                    total_starts,
                    total_earnings,
                    top_rpr,
                    sire_comments[5]]

    df1.loc[horse,:]=table_option1
    
    time.sleep(float(decimal.Decimal(random.randrange(200, 300))/100))

    search_form=browser.find_elements_by_xpath('//a[@class="ui-tabs__tab pp-tabs__tab"]')
    search_form[1].click()

    time.sleep(float(decimal.Decimal(random.randrange(200, 300))/100))

    search_form=browser.find_elements_by_xpath('//a[@class="ui-link ui-link_primary ui-popoverList__link pp-subTabs__tab"]')
    search_form[0].click()

    time.sleep(float(decimal.Decimal(random.randrange(200, 300))/100))
    
    element2 = browser.find_elements_by_xpath("//td[@class='ui-table__cell']")
    titles = [x.text for x in element2]


    info_to_take = ['Flat','Turf','All-weather','Jumps','Chase','Hurdles',
                    'NHF','Broodmare sires','2yo','First Crop','5-6f','7-9f','10-11f',
                    '12-13f','14f+','Heavy','Soft','Gd-sft','Good','Gd-fm','Firm']

    time.sleep(float(decimal.Decimal(random.randrange(150, 300))/100))
    
    for i in info_to_take:
        if i in titles:
            col1 = str(i) + "_win_runners"
            col2 = str(i) + "_wins"
            col3 = str(i) + "_runs"
            col4 = str(i) + "_earnings"

            find_index = titles.index(i)

            win_runners = titles[find_index + 1]
            wins = titles[find_index + 3]
            runs = titles[find_index + 4]
            earnings = titles[find_index + 8]

            df2.loc[horse,[col1, col2, col3, col4]]=[win_runners, wins, runs, earnings]

    return df1, df2


def non_weatherby(browser, horse, df1, df2):
    other_click = browser.find_elements_by_xpath('//button[@class="ui-reset-for-btn ui-modal__closeBtn"]')
    other_click[0].click()

    time.sleep(2)

    search_form=browser.find_elements_by_xpath('//a[@class="ui-tabs__tab pp-tabs__tab hidden-xs-down"]')
    search_form[0].click()

    timeout = 10
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//h2[@class='hp-formTable__title']")))


    element2 = browser.find_elements_by_xpath("//td[@class='ui-table__cell']")
    titles = [x.text for x in element2]
    top_rpr = titles[10]
    total_earnings = titles[7]
    total_starts=titles[1]

    age_element = browser.find_elements_by_xpath("//dt[@class='pp-definition__term']")
    age_element_info = [x.text for x in age_element]
    age=age_element_info[0]

    sire = browser.find_elements_by_xpath("//a[@class='ui-link ui-link_table js-popupLink hp-horseDefinition__link']")
    sire_info = [x.text for x in sire]

    stud = browser.find_elements_by_xpath("//span[@class='hp-nameRow__studFee__value']")
    if not stud:
        stud_fee = 'not there'
    else:
        stud_fee = [x.text for x in stud]

    comments = browser.find_elements_by_xpath("//dd[@class='pp-definition__description']")
    sire_comments = [x.text for x in comments]

    table_option = [age,
                    sire_info[0],
                    sire_info[1],
                    sire_info[2],
                    stud_fee[0],
                    total_starts,
                    total_earnings,
                    top_rpr,
                    sire_comments[5]]


    time.sleep(float(decimal.Decimal(random.randrange(200, 300))/100))

    search_form=browser.find_elements_by_xpath('//a[@class="ui-tabs__tab pp-tabs__tab"]')
    search_form[0].click()

    time.sleep(float(decimal.Decimal(random.randrange(200, 300))/100))

    search_form=browser.find_elements_by_xpath('//a[@class="ui-link ui-link_primary ui-popoverList__link pp-subTabs__tab"]')
    search_form[0].click()

    time.sleep(float(decimal.Decimal(random.randrange(100, 150))/100))

    element2 = browser.find_elements_by_xpath("//td[@class='ui-table__cell']")
    titles = [x.text for x in element2]

    time.sleep(float(decimal.Decimal(random.randrange(150, 300))/100))

    info_to_take = ['Flat','Turf','All-weather','Jumps','Chase','Hurdles',
                    'NHF','Broodmare sires','2yo','First Crop','5-6f','7-9f','10-11f',
                    '12-13f','14f+','Heavy','Soft','Gd-sft','Good','Gd-fm','Firm']


    for i in info_to_take:
        if i in titles:
            col1 = str(i) + "_win_runners"
            col2 = str(i) + "_wins"
            col3 = str(i) + "_runs"
            col4 = str(i) + "_earnings"

            find_index = titles.index(i)

            win_runners = titles[find_index + 1]
            wins = titles[find_index + 3]
            runs = titles[find_index + 4]
            earnings = titles[find_index + 8]

            df2.loc[horse,[col1, col2, col3, col4]]=[win_runners, wins, runs, earnings]
    return df1, df2


def find_the_correct_google_link(browser, horse):
    url2='http://www.google.com'
    browser.get(url2)
        
    time.sleep(2)
    
    search = browser.find_element_by_name('q')
    search.send_keys(str(horse) + ' racing post progeny')
    search.send_keys(Keys.RETURN) # hit return after you enter search text
    
    time.sleep(2)
    
    try:
        search_form=browser.find_elements_by_xpath('//h3[@class="LC20lb DKV0Md"]')
        time.sleep(2)
        search_form[0].click()
    except:
        search_form=browser.find_elements_by_xpath('//h3[@class="LC20lb DKV0Md"]')
        time.sleep(2)
        search_form[4].click()


def racingpost(browser, horse, df1, df2):
    
    time.sleep(3)
    
    find_the_correct_google_link(browser, horse)
    
    time.sleep(3)
    
    timeout = 10
    try:
        weatherby(browser, horse, df1, df2)
    except:
        non_weatherby(browser, horse, df1, df2)


def run_bloodstock(browser, horse_ls, df1, df2):
    failed = []
    i=0

    for horse in horse_ls:
        try:
            racingpost(browser, horse, df1, df2)
        except:
            failed.append(horse)
        i=i+1
        print('{}/{}, failed={}'.format(i, len(horse_ls), len(failed)))

    return df1, df2

