# Extract all dates displayed in the calendar
def get_displayed_dates(browser, by_type, path):
    dates = browser.find_elements(by = by_type, value = path)
    return [date.get_attribute("data-date") for date in dates]