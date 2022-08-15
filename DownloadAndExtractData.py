from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def main():


    UrlList = ["http://prices.super-pharm.co.il/"]
    driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': 'C:/Users/itaba/PycharmProjects/Sooper/SeleniumDownloads'}
    chrome_options.add_experimental_option('prefs', prefs)

    driver.get(UrlList[0])
    links = driver.find_elements(By.CLASS_NAME, "price_item_link")
    links[0].click()

    x = 1
if __name__ == '__main__':
    main()