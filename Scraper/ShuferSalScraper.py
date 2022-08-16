from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from ScraperUtils import *

def DownloadAllPages():
    MainUrl = 'http://prices.shufersal.co.il/?page='
    DownloadPath = r'C:\Users\itaba\Sooper\Scraper\SeleniumDownload'

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory":
                 DownloadPath,  # IMPORTANT - ENDING SLASH V IMPORTANT
             "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service('Scraper/chromedriver.exe'), options=options)


    EmptyDir(DownloadPath)
    PageNum = 1
    while True:
        curUrl = MainUrl + str(PageNum)
        numOfFiles = DownloadOnePage(curUrl, driver)

        if numOfFiles == 0:
            break

        PageNum+=1

    time.sleep(5)


def DownloadOnePage(Url, driver):
    time.sleep(5)
    driver.get(Url)
    time.sleep(5)

    LinksElements = LinksElements = driver.find_elements(By.LINK_TEXT, "לחץ להורדה")
    for LinkElement in LinksElements:
        LinkElement.click()

    return len(LinksElements)




if __name__ == '__main__':

    ExtractAndSaveGzip(r'C:\Users\itaba\Sooper\Scraper\SeleniumDownload\Price7290027600007-001-202208161400.gz')
    DownloadAllPages()