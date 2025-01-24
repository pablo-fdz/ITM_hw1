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
import os
import pandas as pd

# Go get geckodriver from : https://github.com/mozilla/geckodriver/releases

###############################################################################

# PARAMETERS THAT CAN BE MODIFIED

# OS (parameter that just affects the browser start-up). Change to False if not
# Ubuntu
ubuntu_os = True

# Dates selected to do the analysis
start_year = 2025
start_month = 3
end_year = 2025
end_month = 4

# Number of weeks to scrape per month (scraping is not done between months)
num_weeks_to_scrape = 1

# Places selected to do the analysis: Barcelona and Madrid
places = ['Barcelona', 'Madrid, Comunidad de Madrid']

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
# Folder path for general results (the data shown after loading results for a
# location and a date in Booking)
general_results_path = "files/general_results"
# Folder path for URL data (which we will use to access the complete descriptions)
url_data_path = "files/accommodation_urls"


###############################################################################

# NOTE: this scraping has been done for the Spanish regional version of the
# Booking webpage. Its robustness has not been checked for other regions (but it
# should work as long as the website structure is the same)

###############################################################################

# Paths that are used (ordered by appearance)
path_cookies = '//*[@id="onetrust-reject-all-handler"]'
css_calendar = "button.ebbedaf8ac:nth-child(2) > span:nth-child(1)"
path_load_dates = '//div[@id = "calendar-searchboxdatepicker"]//button[@class = "a83ed08757 c21c56c305 f38b6daa18 d691166b09 f671049264 f4552b6561 dc72a8413c f073249358"]'
path_date_selection = '//div[@id="calendar-searchboxdatepicker"]//table[@class="eb03f3f27f"]//tbody//td[@class="b80d5adb18"]//span[@class="cf06f772fa ef091eb985"]'
path_search = '//div[@id="indexsearch"]//div[@class="ffb9c3d6a3 b3b8f00b52 c9a7790c31 e691439f9a"]//button[@class="a83ed08757 c21c56c305 a4c1805887 f671049264 a2abacf76b c082d89982 cceeb8986b b9fd3c6b3c"]'
path_genius = '//div[@class="f0c216ee26 c676dd76fe b5018b639f"]//button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 f4552b6561"]'
path_load_results = '//div[@class="c82435a4b8 f581fde0b8"]//button[@class="a83ed08757 c21c56c305 bf0537ecb5 f671049264 af7297d90d c0e0affd09"]'
path_accomm_box = '//div[@class="c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4"]'
path_main_page = '//header[@class=" Header_root"]//div[@class="Header_logo"]'

# Relative paths to the accommodation boxes (path_accomm_box, ordered by appearance)
rel_path_hotel_name = './/div[@class="f6431b446c a15b38c233"]' # Note that with .// we set it as a relative path to the block_xpath
rel_path_price = './/span[@class="f6431b446c fbfd7c1165 e84eb96b1f"]'
possible_rel_paths_ratings = [
    './/div[@class="a3b8729ab1 d86cee9b25"]',  # First possible XPath (the most common one)
    './/div[@class="a3b8729ab1 e6208ee469 cb2cbb3ccb"]',  # Second possible XPath (external comments)
    ]
rel_path_neighborhood = './/div[@class="abf093bdfe ecc6a9ed89"]//span[@class="aee5343fdb def9bc142a"]'
rel_path_url = './/a[@class="a78ca197d0"]'

###############################################################################

# We generate the date ranges (the dates for which we will scrape information
# from the accommodations)
all_date_ranges = []
for year in range(start_year, end_year + 1):
    for month in range(start_month, end_month + 1):
        all_date_ranges.extend(generate_date_ranges(year, month, num_weeks=num_weeks_to_scrape))

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
        place = place
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

        displayed_dates = get_displayed_dates(browser = browser, by_type = 'xpath', path = path_date_selection)
        while start_date_str not in displayed_dates:
            # Click the button to load more months
            scroll_and_click(browser=browser, by_type='xpath', path=path_load_dates)
            # Refresh displayed dates
            displayed_dates = get_displayed_dates(browser = browser, by_type = 'xpath', path = path_date_selection)

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

            ## Initialize a dictionary with empty lists to store the general 
            ## accommodation results
            accommodation_data = {
                "hotel_name": [],
                "price_euros": [],
                "rating": [],
                # "description": [],
                "neighborhood": [],
                # "start_date": [],
                # "end_date": []
                }

            ## Initialize a dictionary with empty lists to store the name of the
            ## accommodation, the neighborhood (for trying to ensure uniqueness)
            ## and the URL to the accommodation
            url_data = {
                "hotel_name": [],
                "neighborhood": [],
                "url": []
            }

            ## Find all accommodation blocks
            accommodation_blocks = browser.find_elements("xpath", path_accomm_box)

            ## Loop over each accommodation block, setting relative paths to the block_xpath
            for block in accommodation_blocks:
                try:
                    # Extract the hotel name within the block
                    hotel_name = block.find_element(
                        "xpath", rel_path_hotel_name
                    ).text
                except:
                    hotel_name = None  # Handle cases where the hotel name is not found
                
                try:
                    # Extract and clean the price within the block
                    price_string = block.find_element(
                        "xpath", rel_path_price
                    ).text
                    price = float(price_string.split(" ")[1])  # Keep only the numeric part of prices and converting them to floats
                except:
                    price = None  # Handle cases where the price is not found

                # Try to find the rating using multiple possible XPaths
                rating = None  # Default value if no rating is found
                for path_rating in possible_rel_paths_ratings:
                    try:
                        rating_string = block.find_element("xpath", path_rating).text
                        # Clean the rating: keep the last 3 characters and replace commas with dots
                        rating = float(rating_string[-3:].replace(",", "."))
                        if rating:  # If a valid rating is found, exit the loop
                            break
                    except:
                        continue  # Try the next XPath if the current one fails
                
                # Short description in the results list not included in the end
                # (we will include the long one from each accommodation instead)
                # try:
                #     # Extract the description within the block
                #     description = block.find_element(
                #         "xpath", './/div[@class="c19beea015"]'
                #     ).text
                # except:
                #     description = None  # Handle cases where the description is not found

                try:
                    # Extract the neighborhood within the block
                    neighborhood = block.find_element(
                        "xpath", rel_path_neighborhood
                    ).text
                except:
                    neighborhood = None  # Handle cases where the neighborhood is not found
                
                try:
                    # Extract the URL of the accommodation within the block
                    url = block.find_element(
                        "xpath", rel_path_url
                    ).get_attribute("href")
                except:
                    url = None  # Handle cases where the URL is not found

                # Append the data to the dictionary of general results
                accommodation_data["hotel_name"].append(hotel_name)
                accommodation_data["price_euros"].append(price)
                accommodation_data["rating"].append(rating)
                # accommodation_data["description"].append(description)
                accommodation_data["neighborhood"].append(neighborhood)
                # accommodation_data["start_date"].append(start_date_str)
                # accommodation_data["start_date"].append(end_date_str)

                # Append the data to the dictionary of URLS
                url_data["hotel_name"].append(hotel_name)
                url_data["neighborhood"].append(neighborhood)
                url_data["url"].append(url)

            ###################################################################

            # DATA STORAGE in each iteration
            
            ## General results for each accommodation
            df_general_results = pd.DataFrame(accommodation_data)
            # Define the file name with the complete path
            name_general_results = os.path.join(general_results_path, f'results_{start_date_str}_{end_date_str}_{place}.csv')
            df_general_results.to_csv(name_general_results, index = False)
            print("Created general results .csv successfully")

            ## URLs for the accommodations and their names
            df_url = pd.DataFrame(url_data)
            # Define the file name with the complete path
            name_url_data = os.path.join(url_data_path, f'urls_{start_date_str}_{end_date_str}_{place}.csv')
            df_url.to_csv(name_url_data, index = False)
            print("Created URL .csv successfully")

            ###################################################################

            # Go back to the initial booking.com page to repeat the procedure for different dates
            scroll_and_click(browser = browser, by_type = 'xpath', path = path_main_page, delay = 0.75)
            
        else:
            print(f"Could not select date range {start_date_str} - {end_date_str}. Dates not fully visible.")