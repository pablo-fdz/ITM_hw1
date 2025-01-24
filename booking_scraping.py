# We import the auxiliary functions
from auxiliary_functions import (
    generate_date_ranges, get_displayed_dates, load_all_results, 
    scroll_and_click_dates, scroll_and_click, start_up
)

# We import a module that allows to input keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from datetime import datetime
import time
import pandas as pd

# Go get geckodriver from : https://github.com/mozilla/geckodriver/releases

###############################################################################

# PARAMETERS THAT CAN BE MODIFIED

# OS (parameter that just affects the browser start-up). Change to False if not
# Ubuntu
ubuntu_os = True

# Dates selected to do the analysis
start_year = 2025
start_month = 2
end_year = 2025
end_month = 12

# Places selected to do the analysis: Barcelona and Madrid
places = ['Barcelona', 'Madrid']

# Time of sleep (in seconds) between pop-ups screens that may require renderization. 
# A lower time may increase efficiency, but if it's too short it may break the 
# scraping (it decreases robustness)
time_sleep = 2

# Scroll pause between scrolls for loading all results after doing the search
# for a certain location and dates (in seconds). A lower time increases efficienc
# but risks not getting all of the results if the page doesn't load quickly,
# and a longer time increases robustness but reduces efficiency. If it doesn't 
# load all results, try increasing the scroll pause (in seconds)
scroll_pause_load_results = 0.25

# We set as the download directory the folder 'files', defined through a relative 
# path
dfolder = "./files"
# Set the geckodriver path
geko_path = "/usr/local/bin/geckodriver"
# Link to booking
link = "https://www.booking.com/index.es.html"

###############################################################################

# NOTE: this scraping has been done for the Spanish regional version of the
# Booking webpage. Its robustness has not been checked for other regions (but it
# should work as long as the website structure is the same)

###############################################################################

# We generate the date ranges (the dates for which we will scrape information
# from the accommodations)
all_date_ranges = []
for year in range(start_year, end_year + 1):
    for month in range(start_month, end_month + 1):
        all_date_ranges.extend(generate_date_ranges(year, month))

###############################################################################

# Paths that should be fixed in each loop (ordered by appearance)
path_cookies = '//*[@id="onetrust-reject-all-handler"]'
css_calendar = "button.ebbedaf8ac:nth-child(2) > span:nth-child(1)"
path_load_dates = '//div[@id = "calendar-searchboxdatepicker"]//button[@class = "a83ed08757 c21c56c305 f38b6daa18 d691166b09 f671049264 f4552b6561 dc72a8413c f073249358"]'
path_date_selection = '//div[@id="calendar-searchboxdatepicker"]//table[@class="eb03f3f27f"]//tbody//td[@class="b80d5adb18"]//span[@class="cf06f772fa ef091eb985"]'
path_search = '//div[@id="indexsearch"]//div[@class="ffb9c3d6a3 b3b8f00b52 c9a7790c31 e691439f9a"]//button[@class="a83ed08757 c21c56c305 a4c1805887 f671049264 a2abacf76b c082d89982 cceeb8986b b9fd3c6b3c"]'
path_genius = '//div[@class="f0c216ee26 c676dd76fe b5018b639f"]//button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 f4552b6561"]'
path_load_results = '//div[@class="c82435a4b8 f581fde0b8"]//button[@class="a83ed08757 c21c56c305 bf0537ecb5 f671049264 af7297d90d c0e0affd09"]'
path_accomm_box = '//div[@class="c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4"]'
path_main_page = '//header[@class=" Header_root"]//div[@class="Header_logo"]'

###############################################################################

# Start up the browser
browser = start_up(dfolder=dfolder, link=link, geko_path=geko_path, ubuntu = ubuntu_os)

time.sleep(time_sleep)

# We have to reject the cookies to simplify the process of putting buttons into
# view (which is useful when we want to click a button that may be obscured 
# otherwise)
browser.find_element(by="xpath", value= path_cookies).click()

time.sleep(time_sleep)

# Definition of today's date
today = datetime.today()

for place in places:

    # Loop over all date ranges
    for start_date_str, end_date_str in all_date_ranges:

        time.sleep(time_sleep)

        # Convert start and end dates to datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # 1. Check if start_date is in the future (passes if it is)

        if start_date <= today:
            print(f"Skipping date range {start_date_str} - {end_date_str}: Start date is not in the future.")
            continue  # Move to the next week (continue to next iteration)
        
        # 2. Filling fields until the calendar is opened

        # We scroll and click on the "Where are you going?" search button
        scroll_and_click(browser = browser, by_type = 'xpath', path = '//*[@id=":rh:"]')
        # Input the destination for which you want to search accommodations
        place = "Barcelona"
        search1 = browser.find_element(by="xpath", value='//*[@id=":rh:"]')
        search1.send_keys(place)

        # Use ActionChains to press Tab 6 times, to remove the pop-up list that appears
        # to select the destination
        actions = ActionChains(browser)
        for _ in range(6):
            actions.send_keys(Keys.TAB).pause(0.05)
        actions.perform()

        # Scroll and click on the calendar button
        scroll_and_click(browser = browser, by_type = 'css selector', path = css_calendar)

        # 3. Check if the start_date is displayed in the calendar

        displayed_dates = get_displayed_dates(browser)
        while start_date_str not in displayed_dates:
            # Click the button to load more months
            scroll_and_click(browser=browser, by_type='xpath', path=path_load_dates)
            # Refresh displayed dates
            displayed_dates = get_displayed_dates(browser)

        # 4. Select the dates when they are both present and continue scraping 
        # if True

        if start_date_str in displayed_dates and end_date_str in displayed_dates:

            # Scroll and click on the desired dates
            scroll_and_click_dates(browser, "xpath", path_date_selection, start_date_str, end_date_str)

            # Scroll up until calendar button is visible again and click
            scroll_and_click(browser = browser, by_type = 'css selector', path = css_calendar)

            # Once we are outside the date selector, we click on the search button
            browser.find_element(by = "xpath", value = path_search).click()

            time.sleep(time_sleep)

            # We click on the cross to dismiss the Genius pop-up that appears prompting for
            # signing up or signing in. If the button does not exist, it simply continues
            try:
                browser.find_element(by="xpath", value=path_genius).click() # Click the button if it exists
            except:
                pass # Do nothing if the button is not found

            # Load all results that appear on the page
            load_all_results(browser = browser, 
                            button_xpath = path_load_results, 
                            scroll_pause=scroll_pause_load_results)

            # We analyze the data for each accommodation box by box within a loop
            ## Define the XPath for the accommodation boxes

            ## Initialize a dictionary with empty lists to store accommodation data
            accommodation_data = {
                "hotel_name": [],
                "price_euros": [],
                "rating": [],
                "description": [],
                "neighborhood": []
                }

            ## Find all accommodation blocks
            accommodation_blocks = browser.find_elements("xpath", path_accomm_box)

            ## Loop over each accommodation block, setting relative paths to the block_xpath
            for block in accommodation_blocks:
                try:
                    # Extract the hotel name within the block
                    hotel_name = block.find_element(
                        "xpath", './/div[@class="f6431b446c a15b38c233"]' # Note that with .// we set it as a relative path to the block_xpath
                    ).text
                except:
                    hotel_name = None  # Handle cases where the hotel name is not found
                
                try:
                    # Extract and clean the price within the block
                    price_string = block.find_element(
                        "xpath", './/span[@class="f6431b446c fbfd7c1165 e84eb96b1f"]'
                    ).text
                    price = float(price_string.split(" ")[1])  # Keep only the numeric part of prices and converting them to floats
                except:
                    price = None  # Handle cases where the price is not found

                # Try to find the rating using multiple possible XPaths
                rating = None  # Default value if no rating is found
                possible_rating_paths = [
                    './/div[@class="a3b8729ab1 d86cee9b25"]',  # First possible XPath (the most common)
                    './/div[@class="a3b8729ab1 e6208ee469 cb2cbb3ccb"]',  # Second possible XPath (external comments)
                ]
                for path_rating in possible_rating_paths:
                    try:
                        rating_string = block.find_element("xpath", path_rating).text
                        # Clean the rating: keep the last 3 characters and replace commas with dots
                        rating = float(rating_string[-3:].replace(",", "."))
                        if rating:  # If a valid rating is found, exit the loop
                            break
                    except:
                        continue  # Try the next XPath if the current one fails
                
                try:
                    # Extract the description within the block
                    description = block.find_element(
                        "xpath", './/div[@class="c19beea015"]'
                    ).text
                except:
                    description = None  # Handle cases where the description is not found

                try:
                    # Extract the neighborhood within the block
                    neighborhood = block.find_element(
                        "xpath", './/div[@class="abf093bdfe ecc6a9ed89"]//span[@class="aee5343fdb def9bc142a"]'
                    ).text
                except:
                    neighborhood = None  # Handle cases where the neighborhood is not found

                # Append the data to the dictionary
                accommodation_data["hotel_name"].append(hotel_name)
                accommodation_data["price_euros"].append(price)
                accommodation_data["rating"].append(rating)
                accommodation_data["description"].append(description)
                accommodation_data["neighborhood"].append(neighborhood)

            df = pd.DataFrame(accommodation_data)
            df.to_csv("test_results.csv", index = True)
            print("Created .csv successfully")

            # Go back to the initial booking.com page to repeat the procedure for different dates
            scroll_and_click(browser = browser, by_type = 'xpath', path = path_main_page, delay = 0.75)
            
        else:
            print(f"Could not select date range {start_date_str} - {end_date_str}. Dates not fully visible.")