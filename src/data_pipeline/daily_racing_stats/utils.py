import time
import random
import decimal
from selenium.webdriver.common.by import By


def deal_with_popup(browser, css_class, message):
    popup = browser.find_elements(
        By.CSS_SELECTOR, "div[class^='washington-campaign Campaign CampaignType--popup Campaign--css']")
    if len(popup) > 0:
        time.sleep(float(decimal.Decimal(random.randrange(1000, 1300))/100))
        print(message)
        try:
            popup[0].click()
        except:
            browser.find_elements(By.XPATH, "//body")[0].click()
    while len(browser.find_elements(By.CSS_SELECTOR, css_class)) == 0:
        time.sleep(float(decimal.Decimal(random.randrange(1000, 1100))/100))
        if len(popup) > 0:
            try:
                popup[0].click()
            except:
                browser.find_elements(By.XPATH, "//body")[0].click()
        print(message)
