import time

def scroll_and_click(browser, by_type, path, delay=0):
    """
    Scrolls until the given element is visible and clicks on it, with an optional delay.

    Args:
        browser: Selenium WebDriver instance created using the `start_up` function.
        by_type: The type of locator to use (e.g., 'xpath', 'css selector', etc.).
        path: The path to locate the element based on the specified locator type.
        delay: Optional delay (in seconds) before clicking the element. Default is 0.
    """
    try:
        # Find the element using the specified locator type
        element = browser.find_element(by=by_type, value=path)
        
        # Scroll until the element is visible
        browser.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element
        )
        
        # Optional delay before clicking
        if delay > 0:
            time.sleep(delay)
        
        # Click on the element
        element.click()
    except Exception as e:
        print(f"Error while trying to scroll and click: {e}")
