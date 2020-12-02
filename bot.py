import platform
import time

import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def parse_config(path):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(path)

    basic = config._sections['BASIC']
    shipping = config._sections['SHIPPING']
    billing = config._sections['BILLING']

    return basic, shipping, billing


def mount_driver():
    system = platform.system()
    if system == "Windows":
        driver = webdriver.Chrome(r'./chromedriver/chromedriver.exe')
    elif system == "Darwin":
        driver = webdriver.Chrome(r'./chromedriver/chromedriver-mac')
    else:
        driver = webdriver.Chrome(r'./chromedriver/chromedriver-linux')

    return driver


def automate(driver, url, basic, shipping, billing):
    driver.get(url)

    time.sleep(1)
    url = driver.current_url
    if "https://www.walmart.ca/blocked" in url:
        print('Solve the god damn CAPTCHA, hurry up!')

    while "https://www.walmart.ca/blocked" in url:
        time.sleep(1)
        url = driver.current_url

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CLASS_NAME, r"edzik9p0")))

    elements = driver.find_elements(
        By.XPATH, r"/html/body/div[1]/div/div[4]/div/div/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/button[1]")
    if elements:
        xpath = r"/html/body/div[1]/div/div[4]/div/div/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/button[1]"
    else:
        xpath = r"/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/button[1]"

    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.XPATH, xpath)))

    while not(element.is_enabled()):
        driver.refresh()
        element = WebDriverWait(driver, 120).until(EC.presence_of_element_located(
            (By.XPATH, xpath)))

    element.click()

    time.sleep(1)
    url = driver.current_url
    if "https://www.walmart.ca/blocked" in url:
        print('You have 2 minutes to solve the god damn CAPTCHA, hurry up!')
        WebDriverWait(driver, 120).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div/div[4]/div/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/div/button[1]"))).click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='atc-root']/div[3]/div[2]/button[1]"))).click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"/html/body/div[1]/div/div/div[3]/div[4]/div[2]/div/div[1]/div[11]/a/button"))).click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='email']"))).send_keys(basic['email'])

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='step1']/div[2]/form/div/div[5]/button"))).click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='shipping-tab']/div/div/div"))).click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='firstName']"))).send_keys(shipping['first_name'])

    driver.find_element_by_xpath(
        "//*[@id='lastName']").send_keys(shipping['last_name'])

    driver.find_element_by_xpath(
        "//*[@id='address1']").send_keys(shipping['address1'])

    driver.find_element_by_xpath(
        "//*[@id='address2']").send_keys(shipping['address2'])

    driver.find_element_by_xpath("//*[@id='city']").send_keys(shipping['city'])

    Select(driver.find_element_by_xpath(
        "//*[@id='province']")).select_by_visible_text(shipping['province'])

    driver.find_element_by_xpath(
        "//*[@id='postalCode']").send_keys(shipping['postal_code'])

    driver.find_element_by_xpath(
        "//*[@id='phoneNumber']").send_keys(shipping['phone'])

    driver.find_element_by_xpath("//*[@id='save']").click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='shippingAddressForm']/div[3]/button"))).click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='step2']/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/button"))).click()

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='cardNumber']"))).send_keys(billing['card_number'])
    driver.find_element_by_xpath(
        "//*[@id='expiryMonth']").send_keys(billing['expiry_month'])
    driver.find_element_by_xpath(
        "//*[@id='expiryYear']").send_keys(billing['expiry_year'])
    driver.find_element_by_xpath(
        "//*[@id='securityCode']").send_keys(billing['security_code'])

    WebDriverWait(driver, 120).until(EC.presence_of_element_located(
        (By.XPATH, r"//*[@id='billingForm']/div/button"))).click()

    WebDriverWait(driver, 120).until(EC.element_to_be_clickable(
        (By.XPATH, r"/html/body/div[1]/div/div/div[1]/div[3]/div/div/div/button"))).click()


if __name__ == "__main__":
    print('Make sure your settings.ini file is configured correctly')
    print('Reading settings.ini...')
    basic, shipping, billing = parse_config(r'./settings.ini')

    print('Please enter desired Walmart URL')
    url = input('url: ')

    driver = mount_driver()
    automate(driver, url, basic, shipping, billing)
