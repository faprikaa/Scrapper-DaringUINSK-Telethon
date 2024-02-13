import traceback

from selenium.common import UnexpectedAlertPresentException, ElementNotInteractableException
from selenium.webdriver.common.by import By

from core.browser import browser


def click_next():
    button = browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[12]/center/button")
    try:
        click = button.click()
        return("Tombol Perlihatkan Sebelumnya berhasil di klik kali !!")
    except UnexpectedAlertPresentException:
        return("Cookies habis silahkan login ulang")
    except ElementNotInteractableException:
        return("Please wait 10 seconds before send this command again")
    except:
        return(f"An error occured at next, {traceback.format_exc()}")