import time
import random
import decimal
import json
import hashlib
from selenium.webdriver.common.by import By

from utils import deal_with_popup


class Horse:
    def __init__(self, browser, race_name, winnings_json, race_type):
        self.browser = browser
        self.race_name = race_name
        self.winnings_json = winnings_json
        self.race_type = race_type

    def get_horse_id(self):
        hash_object = hashlib.md5(self.horse_name.encode())
        return hash_object.hexdigest()

    def get_horse_winnings(self):
        winnings_dict = json.loads(self.winnings_json)
        if str(self.position) in winnings_dict.keys():
            return winnings_dict[str(self.position)]
        else:
            return 0

    def get_runner_info(self, runner_info):
        """ 
        gets information for selected horse in the race
        """
        position, beaten_by, stall_number, horse_number, horse_name, age_weight, sp, trainer_jockey, race_comments = self.get_right_runner_config(
            runner_info)

        if (len(age_weight) <= 6) & (age_weight[2] not in ['7', '8', '9']):
            weight = age_weight[1:]
            age = age_weight[0]
        else:
            age = age_weight[0:2]
            weight = age_weight[2:]

        tj_split = trainer_jockey.split('J: ')

        self.browser.current_url.split('/')
        self.date = self.browser.current_url.split('/')[5]
        self.track = self.browser.current_url.split('/')[6]

        self.trainer = tj_split[0].replace('T: ', '')
        self.jockey = tj_split[1]
        if position in ['PU', 'F']:
            self.position = position
        else:
            self.position = position[:-2]
        self.horse_name = horse_name
        self.horse_id = self.get_horse_id()
        self.horse_age = age
        self.horse_weight = weight
        self.beaten_by = beaten_by
        self.sp = sp
        self.race_comments = race_comments

        self.winnings = self.get_horse_winnings()
        self.stall_number = stall_number
        self.estimated_running_time = "TODO"

    def get_right_runner_config(self, runner_info):
        if self.race_type in ['Chase', 'Hurdle', 'NHF', 'NH', 'NH Flat Race']:
            if len(runner_info) == 9:
                [horse_position, horse_number, horse_name, age_weight, sp,
                    trainer_jockey, race_comments, text, text2] = runner_info
                beaten_by = 'N/A'
                stall_number = 'N/A'

            elif len(runner_info) == 10:
                [horse_position, beaten_by, horse_number, horse_name, age_weight,
                    sp, trainer_jockey, race_comments, text, text2] = runner_info
                stall_number = 'N/A'
        else:
            if len(runner_info) == 10:
                [horse_position, horse_number, stall_number, horse_name, age_weight,
                    sp, trainer_jockey, race_comments, text, text2] = runner_info
                beaten_by = 'N/A'

            elif len(runner_info) == 11:
                [horse_position, beaten_by, horse_number, stall_number, horse_name,
                    age_weight, sp, trainer_jockey, race_comments, text, text2] = runner_info

        try:
            return horse_position, beaten_by, stall_number, horse_number, horse_name, age_weight, sp, trainer_jockey, race_comments
        except:
            return print(runner_info)

    def get_breeding_info(self):
        # Links to click on the horse
        deal_with_popup(
            self.browser, "div[class^='ResultRunner__StyledHorseName-sc-58kifh-5']", "popup checking horse main page")
        horseLinks = self.browser.find_elements(By.XPATH, "//a")
        selectedHorse = [i for i in horseLinks if i.text == self.horse_name]
        if len(selectedHorse) > 0:
            time.sleep(float(decimal.Decimal(random.randrange(20, 50))/100))
            self.browser.execute_script(
                "arguments[0].click();", selectedHorse[0])

        time.sleep(float(decimal.Decimal(random.randrange(200, 700))/100))
        deal_with_popup(
            self.browser, "table[class^='Header__DataTable']", "popup checking horse breeding page")
        # get breeding info for the horse
        breeding_info = self.browser.find_elements(
            By.CSS_SELECTOR, "table[class^='Header__DataTable']")[0].text.split('\n')
        [age2, trainer2, horse_sex, sire, dam, owner] = breeding_info

        self.horse_sex = horse_sex.split(' ')[1]
        self.sire = " ".join(sire.split(' ')[1:])
        self.dam = " ".join(dam.split(' ')[1:])
        self.owner = " ".join(owner.split(' ')[1:])
        self.browser.back()
        time.sleep(float(decimal.Decimal(random.randrange(100, 500))/100))

    def add_to_df(self, df):
        """ 
        appends row to pandas dataframe
        TODO: this will change to append row to postgres table using sqlalchemy
        """
        row_dict = {
            "date": self.date,
            "race_name": self.race_name,
            "track": self.track,
            "horse_id": self.horse_id,
            "horse_name": self.horse_name,
            "horse_age": self.horse_age,
            "horse_sex": self.horse_sex,
            "dam": self.dam,
            "sire": self.sire,
            "owner": self.owner,
            "trainer": self.trainer,
            "jockey": self.jockey,
            "weight": self.horse_weight,
            "sp": self.sp,
            "position": self.position,
            "beaten_by": self.beaten_by,
            "winnings": self.winnings,
            "stall_number": self.stall_number,
            "race_comments": self.race_comments,
            "estimated_running_time": self.estimated_running_time
        }
        df = df.append(row_dict, ignore_index=True)
        return df
