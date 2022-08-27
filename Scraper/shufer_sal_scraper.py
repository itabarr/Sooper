from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from scraper.scraper_utils import *

def download_all_pages(download_path, main_url):

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory":
                 download_path,  # IMPORTANT - ENDING SLASH V IMPORTANT
             "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)

    empty_dir(download_path)
    driver.get(main_url)
    last_page_num = get_last_page(driver)

    PageNum = 1
    while True:
        print(f'Download page number {PageNum}.')
        curUrl = main_url + str(PageNum)

        numOfFiles = download_one_page(curUrl, driver)
        if numOfFiles == 0:
            break


        if PageNum == last_page_num:
            break
        PageNum += 1
    time.sleep(5)
def download_one_page(url, driver):
    time.sleep(5)
    driver.get(url)
    time.sleep(5)

    LinksElements = driver.find_elements(By.LINK_TEXT, "לחץ להורדה")
    for LinkElement in LinksElements:
        LinkElement.click()

    return len(LinksElements)
def get_last_page(driver):
    elem = driver.find_element(By.LINK_TEXT, ">>")
    last_page_num = int(elem.get_attribute('href').split('=')[-1])

    return last_page_num

if __name__ == '__main__':
    MAIN_URL = 'http://prices.shufersal.co.il/?page='
    DOWNLOAD_PATH = r'C:\Users\as\Sooper\SeleniumDownload'

    download_all_pages(DOWNLOAD_PATH, MAIN_URL)
    extract_dir(DOWNLOAD_PATH)