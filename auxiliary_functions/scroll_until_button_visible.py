import time

def scroll_until_button_visible(browser, button_xpath, scroll_pause=0.1, max_attempts=50):
    """
    Scrolls down the page until the "Load more results" button becomes visible.

    This function repeatedly scrolls down the page by the height of the visible window 
    using `window.scrollBy(0, window.innerHeight)`. After each scroll, it checks whether 
    the specified button is visible. If the button is found and displayed, the function 
    exits successfully. A pause (`scroll_pause`) is added between scrolls to allow time 
    for additional content to load. To avoid infinite loops, a maximum number of scroll 
    attempts (`max_attempts`) is defined.

    Args:
        browser: Selenium WebDriver instance.
        button_xpath: XPath of the "Load more results" button to locate.
        scroll_pause: Time (in seconds) to pause between scroll actions. Default is 1 second.
        max_attempts: Maximum number of scroll attempts before stopping. Default is 50.

    Returns:
        bool: True if the button is found and visible, False otherwise.

    Example Usage:
        path = '//div[@class="c82435a4b8 f581fde0b8"]//button[@class="a83ed08757 c21c56c305 bf0537ecb5 f671049264 af7297d90d c0e0affd09"]'

        if scroll_until_button_visible(browser, path):
            scroll_and_click(browser=browser, by_type='xpath', path=path)
        else:
            print("Load more results button not found.")
    """
    attempts = 0
    button_found = False

    while attempts < max_attempts:
        # Scroll down to load more results
        browser.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(scroll_pause)  # Pause to allow loading of content

        try:
            # After scrolling, try to find the button
            button = browser.find_element(by="xpath", value=button_xpath)
            if button.is_displayed():
                button_found = True
                break  # Button found and clicked
        except:
            pass  # Ignore errors if the button is not found yet

        attempts += 1

    if button_found:
        return True
    else:
        print("Reached maximum attempts or button not found.")
        return False