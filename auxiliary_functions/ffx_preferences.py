import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Function for defining the Firefox preferences: we initialize a blank browser
# with a new profile
def ffx_preferences(dfolder, download=False):
    """
    Sets the preferences of the firefox browser: download path.
    """
    profile = webdriver.FirefoxProfile()
    # set download folder:
    profile.set_preference(
        "browser.download.dir", dfolder
    )  # you can predefine where you wanna store things in case its needed
    profile.set_preference(
        "browser.download.folderList", 2
    )  # 0 means to download to the desktop, 1 means to download to the default "Downloads" directory, 2 means to use the directory
    profile.set_preference(
        "browser.download.manager.showWhenStarting", False
    )  # I dont wanna see a pop up for each download so i swicth it off
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/msword,application/rtf, application/csv,text/csv,image/png ,image/jpeg, application/pdf, text/html,text/plain,application/octet-stream",
    )

    # profile.install_addon('/Users/luisignaciomenendezgarcia/Dropbox/CLASSES/class_bse_text_mining/class_scraping_bse_2025/booking/booking/ublock_origin-1.55.0.xpi')
    # profile.add_extension('/Users/luisignaciomenendezgarcia/Dropbox/CLASSES/class_bse_text_mining/class_scraping_bse/booking/booking/ublock_origin-1.55.0.xpi')

    # this allows to download pdfs automatically
    if download:
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/pdf,application/x-pdf",
        )
        profile.set_preference(
            "pdfjs.disabled", True
        )  # dont want the pdf viewer to open

    options = Options()
    options.profile = profile
    # We indicate the location of the Firefox executable
    # options.binary_location = r"/usr/bin/firefox"
    return options