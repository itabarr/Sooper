from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from Scraper.ScraperUtils import *

def DownloadAllPages(DownloadPath , MainUrl):

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory":
                 DownloadPath,  # IMPORTANT - ENDING SLASH V IMPORTANT
             "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)


    EmptyDir(DownloadPath)
    driver.get(MainUrl)
    last_page_num = GetLastPage(driver)

    PageNum = 1
    while True:
        print(f'Download page number {PageNum}.')
        curUrl = MainUrl + str(PageNum)

        numOfFiles = DownloadOnePage(curUrl, driver)
        if numOfFiles == 0:
            break


        if PageNum == last_page_num:
            break
        PageNum += 1
    time.sleep(5)


def DownloadOnePage(Url, driver):
    time.sleep(5)
    driver.get(Url)
    time.sleep(5)

    LinksElements = driver.find_elements(By.LINK_TEXT, "לחץ להורדה")
    for LinkElement in LinksElements:
        LinkElement.click()

    return len(LinksElements)


def GetLastPage(driver):
    elem = driver.find_element(By.LINK_TEXT, ">>")
    last_page_num = int(elem.get_attribute('href').split('=')[-1])

    return last_page_num

if __name__ == '__main__':
    MainUrl = 'http://prices.shufersal.co.il/?page='
    DownloadPath = r'C:\Users\as\Sooper\SeleniumDownload'

    DownloadAllPages(DownloadPath, MainUrl)
    ExtractDir(DownloadPath)