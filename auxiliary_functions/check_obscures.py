from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)

def check_obscures(browser, xpath, type):
    """
    Function that checks whether the object is being "obscured" by any element so
    that it is not clickable. Important: if True, the object is going to be clicked!
    """
    try:
        if type == "xpath":
            browser.find_element("xpath", xpath).click()
        elif type == "id":
            browser.find_element("id", xpath).click()
        elif type == "css":
            browser.find_element("css selector", xpath).click()
        elif type == "class":
            browser.find_element("class name", xpath).click()
        elif type == "link":
            browser.find_element("link text", xpath).click()
    except (
        ElementClickInterceptedException,
        NoSuchElementException,
        StaleElementReferenceException,
    ) as e:
        print(e)
        return False
    return True