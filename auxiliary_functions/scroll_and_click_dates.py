def scroll_and_click_dates(browser, by_type, path, start_date, end_date):
    """
    Scrolls through a calendar, finds specified dates, and clicks on them.

    Args:
        browser: Selenium WebDriver instance.
        by_type: Locator type (e.g., 'xpath', 'css selector', etc.).
        path: Locator path to identify all date elements.
        start_date: Start date as a string (e.g., "2025-01-24").
        end_date: End date as a string (e.g., "2025-01-31").
    """
    try:
        # Find all dates matching the given path
        dates = browser.find_elements(by=by_type, value=path)
        
        # Iterate over the dates and click the start and end dates
        for date in dates:
            current_date = date.get_attribute("data-date")
            if current_date == start_date or current_date == end_date:
                # Scroll to the specific date
                browser.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", date
                )
                # Click on the date
                date.click()
                # Stop if the end date is clicked
                if current_date == end_date:
                    break
    except Exception as e:
        print(f"Error while scrolling and clicking on dates: {e}")