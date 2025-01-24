# Extract all dates displayed in the calendar
def get_displayed_dates(browser):
    path = '//div[@id="calendar-searchboxdatepicker"]//table[@class="eb03f3f27f"]//tbody//td[@class="b80d5adb18"]//span[@class="cf06f772fa ef091eb985"]'
    dates = browser.find_elements("xpath", path)
    return [date.get_attribute("data-date") for date in dates]