import time
import random
import decimal
import json
import hashlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from utils import deal_with_popup
from race import Race
from horse import Horse


class Day:
    def __init__(self, browser, date, race_df, horse_df):
        self.browser = browser
        self.date = date
        self.race_df = race_df
        self.horse_df = horse_df

    def get_stats(self):
        """ 
        date needs to be format yyyy-mm-dd 2021-12-05
        """
        url_date = str(self.date).split(' ')[0]
        self.browser.get(
            f'https://www.sportinglife.com/racing/results/{url_date}')
        time.sleep(float(decimal.Decimal(random.randrange(200, 300))/100))
        cookies_button = self.browser.find_elements(
            By.CSS_SELECTOR, "button[class^='BaseButton__BaseButtonStyled-e225m1-0']")
        if len(cookies_button) > 0:
            cookies_button[0].click()
        num_races = len(self.browser.find_elements(
            By.CSS_SELECTOR, "span[class^='Race__RaceTime-sc-16yubq3-1']"))
        race_selectors = ["span[class^='Race__RaceTime-sc-16yubq3-1']",
                          "div[class^='FutureRace__RaceName-sc-1yen8s9-0']",
                          "div[class^='FutureRace__RaceDetailsContainer-sc-1yen8s9-1']"]  # this gives impression of clicking on different parts of the race button

        for i in range(0, num_races):
            # First get info for the race itself
            timeout = 10
            idx = random.randint(0, 2)
            WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, race_selectors[idx])))
            self.browser.refresh()
            time.sleep(float(decimal.Decimal(random.randrange(100, 200))/100))
            deal_with_popup(
                self.browser, race_selectors[idx], "popup checking 1")
            races = self.browser.find_elements(
                By.CSS_SELECTOR, race_selectors[idx])

            time.sleep(float(decimal.Decimal(random.randrange(20, 50))/100))
            self.browser.execute_script("arguments[0].click();", races[i])
            time.sleep(float(decimal.Decimal(random.randrange(500, 1000))/100))
            new_race = Race(self.browser)
            new_race.get_race_info()

            self.race_df = new_race.add_to_df(self.race_df)
            # print(self.race_df.tail(1))
            # Now get info for each runner in the race
            num_runners = len(self.browser.find_elements(
                By.CSS_SELECTOR, "div[class^='ResultRunner__StyledResultRunner']"))
            for runs_idx in range(0, num_runners):
                deal_with_popup(
                    self.browser, "div[class^='ResultRunner__StyledResultRunner']", "popup checking 2")
                runners = self.browser.find_elements(
                    By.CSS_SELECTOR, "div[class^='ResultRunner__StyledResultRunner']")
                if len(runners) == 0:
                    self.browser.refresh()
                    time.sleep(float(decimal.Decimal(
                        random.randrange(100, 200))/100))
                runner = runners[runs_idx]
                runner_info = runner.text.split('\n')
                horse = Horse(self.browser, new_race.race_name,
                              new_race.prize_money_json, new_race.race_type)
                deal_with_popup(
                    self.browser, "div[class^='ResultRunner__StyledResultRunner']", "popup checking 3")
                if len(runner_info) == 0:
                    runner = self.browser.find_elements(
                        By.CSS_SELECTOR, "div[class^='ResultRunner__StyledResultRunner']")[runs_idx]
                    runner_info = runner.text.split('\n')
                horse.get_runner_info(runner_info)
                horse.get_breeding_info()
                print(horse.horse_name)
                self.horse_df = horse.add_to_df(self.horse_df)

            # print(self.horse_df.tail(1))
            self.browser.back()
            time.sleep(float(decimal.Decimal(random.randrange(500, 1200))/100))
        return self.race_df, self.horse_df
