from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

from src.bloodstock import (weatherby,
                            non_weatherby,
                            find_the_correct_google_link,
                            racingpost,
                            run_bloodstock
                            )

from src.data import create_df1_template, create_df2_template, horse_ls

chrome_options = Options()
chrome_options.add_argument("--headless")
df1 = create_df1_template()
df2 = create_df2_template()


if __name__ == '__main__':
    browser = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    browser.get('http://www.racingpost.com')
    search_form = browser.find_elements(
        '//a[@class="CybotCookiebotDialogBodyButton"]')
    time.sleep(1)
    search_form[1].click()
    print('Initialising chrome')
    df1, df2 = run_bloodstock(browser, horse_ls, df1, df2)
    df1.to_csv('~/Downloads/stallion_basic_stats.csv')  # TODO add to database
    # TODO add to database
    df2.to_csv('~/Downloads/stallion_progeny_stats.csv')
    print('Finished scraping')
