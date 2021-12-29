from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd

from day import Day

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')

if __name__ == '__main__':
    browser = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    date_range = pd.date_range('2021-11-08', periods=1)
    for date in date_range:
        print(f'getting stats for {date}')
        day = Day(browser, date, race_df, horse_df)
        race_df, horse_df = day.get_stats()
