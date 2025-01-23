# We import the auxiliary functions
from auxiliary_functions import (
    generate_date_ranges, load_all_results, scroll_and_click_dates, 
    scroll_and_click, start_up
)

# We import a module that allows to input keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import pandas as pd

# Go get geckodriver from : https://github.com/mozilla/geckodriver/releases

# We set as the download directory the folder 'files',
# defined through a relative path
dfolder = "./files"
# Set the geckodriver path
geko_path = "/usr/local/bin/geckodriver"
# Link to booking
link = "https://www.booking.com/index.es.html"

browser = start_up(dfolder=dfolder, link=link, geko_path=geko_path, ubuntu = True)

time.sleep(2)  # Wait up to 2 seconds for elements to appear

# We have to reject the cookies to simplify the process of putting buttons into
# view (which is useful when we want to click a button that may be obscured 
# otherwise)
path = '//*[@id="onetrust-reject-all-handler"]'
browser.find_element(by="xpath", value= path).click()

time.sleep(1.5)  # Wait up to 1.5 seconds for elements to appear

# Places selected to do the analysis: Barcelona and Madrid
places = ['Barcelona', 'Madrid']

# Dates selected to do the analysis
start_year = 2025
start_month = 2
end_year = 2025
end_month = 12

all_date_ranges = []
for year in range(start_year, end_year + 1):
    for month in range(start_month, end_month + 1):
        all_date_ranges.extend(generate_date_ranges(year, month))

# Use in scraping
for start_date, end_date in all_date_ranges:
    print(f"Scraping for dates {start_date} to {end_date}...")
    # Call your scraping function here with start_date and end_date

for place in places:

    for date in dates:

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
        css = "button.ebbedaf8ac:nth-child(2) > span:nth-child(1)"
        scroll_and_click(browser = browser, by_type = 'css selector', path = css)

        # We select the dates
        ## Set the path for the date buttons
        path = '//div[@id="calendar-searchboxdatepicker"]//table[@class="eb03f3f27f"]//tbody//td[@class="b80d5adb18"]//span[@class="cf06f772fa ef091eb985"]'
        ## Set the dates (yyyy-mm-dd)
        start_date = f"2025-01-24"
        end_date = f"2025-01-31"
        ## Scroll for visibility and click on the desired dates
        scroll_and_click_dates(browser, "xpath", path, start_date, end_date)

        # Scroll up until calendar button is visible again and click
        css = "button.ebbedaf8ac:nth-child(2) > span:nth-child(1)"
        scroll_and_click(browser = browser, by_type = 'css selector', path = css)

        # Once we are outside the date selector, we click on the search button
        my_xpath = '//div[@id="indexsearch"]//div[@class="ffb9c3d6a3 b3b8f00b52 c9a7790c31 e691439f9a"]//button[@class="a83ed08757 c21c56c305 a4c1805887 f671049264 a2abacf76b c082d89982 cceeb8986b b9fd3c6b3c"]'
        browser.find_element(by = "xpath", value = my_xpath).click()

        time.sleep(2)  # Wait up to 2 seconds for elements to appear

        # We click on the cross to dismiss the Genius pop-up that appears prompting for
        # signing up or signing in. If the button does not exist, it simply continues
        path = '//div[@class="f0c216ee26 c676dd76fe b5018b639f"]//button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 f4552b6561"]'
        try:
            browser.find_element(by="xpath", value=path).click() # Click the button if it exists
        except:
            pass # Do nothing if the button is not found

        # Load all results that appear on the page
        path = '//div[@class="c82435a4b8 f581fde0b8"]//button[@class="a83ed08757 c21c56c305 bf0537ecb5 f671049264 af7297d90d c0e0affd09"]'
        # If it doesn't load all results, try increasing the scroll pause (in seconds)
        # Efficiency increases by reducing the scroll pause, at the cost of possibly 
        # not getting all of the results if the page doesn't load quickly
        load_all_results(browser = browser, 
                        button_xpath = path, 
                        scroll_pause=0.25)

        # We analyze the data for each accommodation box by box within a loop
        ## Define the XPath for the accommodation blocks
        block_xpath = '//div[@class="c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4"]'

        ## Initialize a dictionary with empty lists to store accommodation data
        accommodation_data = {
            "hotel_name": [],
            "price_euros": [],
            "rating": [],
            "description": [],
            "neighborhood": []
            }

        ## Find all accommodation blocks
        accommodation_blocks = browser.find_elements("xpath", block_xpath)

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
            for path in possible_rating_paths:
                try:
                    rating_string = block.find_element("xpath", path).text
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
        path = '//header[@class=" Header_root"]//div[@class="Header_logo"]'
        scroll_and_click(browser = browser, by_type = 'xpath', path = path)