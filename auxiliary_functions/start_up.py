import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from .ffx_preferences import ffx_preferences

def start_up(link, dfolder, geko_path, download=True, ubuntu = False):
    os.makedirs(dfolder, exist_ok=True)

    if ubuntu == True:
        # Set TMPDIR environment variable for sandboxed Firefox (Snap package, for
        # Ubuntu users)
        os.environ["TMPDIR"] = os.path.expanduser("~/tmp")

    # Get Firefox options, including download preferences if applicable
    options = ffx_preferences(dfolder, download)

    service = Service(geko_path)
    browser = webdriver.Firefox(service=service, options=options)

    # Enter the website address here
    browser.get(link)
    time.sleep(5)  # Adjust sleep time as needed
    return browser