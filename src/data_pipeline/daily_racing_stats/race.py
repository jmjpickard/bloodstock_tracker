
import json
from selenium.webdriver.common.by import By
from currency_converter import CurrencyConverter
from typing import List

from utils import deal_with_popup


class Race:
    def __init__(self, browser):
        self.browser = browser

    def get_race_info(self):
        self.browser.current_url.split('/')
        self.date = self.browser.current_url.split('/')[5]
        self.track = self.browser.current_url.split('/')[6]
        deal_with_popup(
            self.browser, "div[class^='RacePage__SummaryWrapper']", "popup checking race")
        race_info = self.browser.find_elements(
            By.CSS_SELECTOR, "div[class^='RacePage__SummaryWrapper']")[0].text.split('\n')

        self.race_name = race_info[0]
        race_sub_info = self.get_variable_race_sub_info(
            race_info[1].split('  |   '))
        self.race_age_group = race_sub_info[0]
        self.race_class = race_sub_info[1]
        self.distance = self.get_distance_in_yards(race_sub_info[2])
        self.going = race_sub_info[3]
        self.runners = race_sub_info[4].split(' ')[0]
        self.track_type = race_sub_info[5]
        timing = race_info[3].split('  |   ')
        self.off_time = timing[0].split(': ')[1]
        self.winning_time = self.get_time_in_seconds(timing[1].split(': ')[1])
        self.race_type = self.get_race_type()
        prize_money = self.get_prize_money_dict()
        self.prize_money_json = json.dumps(prize_money)
        self.purse = sum(prize_money.values())

    def get_race_type(self):
        lower_case_race_name = self.race_name.lower()
        if "chase" in lower_case_race_name:
            return "Chase"
        elif "hurdle" in lower_case_race_name:
            return "Hurdle"
        elif ('nhf' in lower_case_race_name) | ('flat' in lower_case_race_name):
            return "NHF"
        else:
            return "Flat"

    def get_variable_race_sub_info(self, race_sub_info: List[str]) -> List[str]:
        """ 
        Deals with issue where Irish courses don't use race class so need to set that as N/A
        """
        if len(race_sub_info) == 5:
            [race_age_group, distance, going, num_runners, track] = race_sub_info
            class_of_race = 'N/A'
        else:
            [race_age_group, class_of_race, distance,
                going, num_runners, track] = race_sub_info

        return [race_age_group, class_of_race, distance, going, num_runners, track]

    def get_time_in_seconds(self, winning_time: str) -> float:
        """
        Input looks like this '5m 6.71s' -> convert to total seconds
        """
        if len(winning_time.split(' ')) == 1:
            seconds = float(winning_time.replace('s', ''))
            self.winning_time = seconds
            return seconds
        else:
            [min, sec] = winning_time.split(' ')
            min_to_seconds = int(min.replace('m', '')) * 60
            seconds = float(sec.replace('s', ''))
            total_time = min_to_seconds + seconds
            self.winning_time = total_time
            return total_time

    def get_distance_in_yards(self, distance: str) -> int:
        """ 
        Converts the race distance to yards for ease of analysis
        """
        segments = distance.split(' ')
        race_yards = 0
        for item in segments:
            if 'm' in item:
                miles = item.replace('m', '')
                miles_to_yards = int(miles) * 1760
                race_yards += miles_to_yards
            elif 'f' in item:
                furlongs = item.replace('f', '')
                furlongs_to_yards = int(furlongs) * 220
                race_yards += furlongs_to_yards
            elif 'y' in item:
                yards = item.replace('y', '')
                race_yards += int(yards)
        return race_yards

    def get_winnings_in_gbp(self, winnings_string: str) -> float:
        """ 
        Where prize money is in euros, convert to gbp using the currency converter API 
        (uses European Central Bank rates)
        """
        c = CurrencyConverter()
        winning_val = winnings_string[1:].replace(',', '')
        if winnings_string[0] == '€':
            winnings = float(winning_val)
            return c.convert(winnings, 'EUR', 'GBP')
        else:
            return float(winning_val)

    def get_prize_money_dict(self) -> dict:
        """ 
        Gets the prize money for the race and returns dict of {'position': 'winnings'}
        """
        prize_money_elements = self.browser.find_elements(
            By.CSS_SELECTOR, "div[class^='PrizeMoney__PrizeSummary-sc-199orl7-3']")[0].text.split('\n')
        prize_money = {}
        for i, item in enumerate(prize_money_elements):
            if (i % 2 == 0) | (i == 0):
                # removes text just leaves the position number as a string
                key = prize_money_elements[i][:-3]
                val = prize_money_elements[i+1]
                prize_money[key] = self.get_winnings_in_gbp(
                    winnings_string=val)

        return prize_money

    def add_to_df(self, df):
        """ 
        appends row to pandas dataframe
        TODO: this will change to append row to postgres table using sqlalchemy
        """
        row_dict = {
            "date": self.date,
            "track": self.track,
            "race_name": self.race_name,
            "race_age_group": self.race_age_group,
            "race_class": self.race_class,
            "distance": self.distance,
            "going": self.going,
            "runners": self.runners,
            "track_type": self.track_type,
            "race_type": self.race_type,
            "off_time": self.off_time,
            "winning_time": self.winning_time,
            "prize_money_json": self.prize_money_json,
            "purse": self.purse
        }
        df = df.append(row_dict, ignore_index=True)
        return df
