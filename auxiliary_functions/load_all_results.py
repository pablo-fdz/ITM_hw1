from .scroll_until_button_visible import scroll_until_button_visible
from .scroll_and_click import scroll_and_click

def load_all_results(browser, button_xpath, scroll_pause=0.1, max_attempts=50):
    # Scroll down and click in the Load more results" button

    # Initialize variables
    click_count = 0  # Counter for the number of button clicks

    # Loop until button is no longer visible
    while True:
        if scroll_until_button_visible(
            browser = browser, button_xpath = button_xpath, 
            scroll_pause = scroll_pause, max_attempts = max_attempts):
            scroll_and_click(browser=browser, by_type='xpath', path=button_xpath)
            click_count += 1
            
        else:
            break  # Exit the loop if no button is found

    # Print the final click count
    print(f"Total 'Load more results' button clicks: {click_count}.")