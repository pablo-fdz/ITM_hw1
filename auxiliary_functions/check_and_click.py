from .check_obscures import check_obscures
import time

def check_and_click(browser, xpath, type):
    """
    Function that checks whether the object is clickable and, if so, clicks on
    it. If not, waits one second and tries again.
    """
    ck = False
    ss = 0
    while ck == False:
        ck = check_obscures(browser, xpath, type)
        time.sleep(1)
        ss += 1
        if ss == 15:
            # warn_sound()
            # return NoSuchElementException
            ck = True
            # browser.quit()