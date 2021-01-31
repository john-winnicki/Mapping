from selenium import webdriver                    # Import module 
from selenium.webdriver.common.keys import Keys   # For keyboard keys 
import time                                       # Waiting function  

URL = 'https://purl.stanford.edu/mr870gt3467'      # Define URL 
browser = webdriver.Chrome()                       # Create driver object means open the browser 

browser.get(URL)
time.sleep(5)

browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))

time.sleep(1)

browser.find_element_by_xpath("/html/body/div/div/div/div/main/div[1]/div[1]/section/div[1]/header/nav/div/button[3]").click()

# element = browser.find_element_by_xpath("//button[@aria-label='Share & download']")
# element_text = element.text
# element_attribute_value = element.get_attribute('value')
# print(element)
# print('element.text: {0}'.format(element_text))
# print('element.get_attribute(\'value\'): {0}'.format(element_attribute_value))
# browser.quit()

# browser.find_element_by_xpath("//a[@class='btn btn-secondary']").click()
# print(browser.page_source)

time.sleep(1)

browser.find_element_by_xpath("/html/body/div/div/div/div/main/div[3]/div[3]/ul/li[2]").click()

time.sleep(1)

browser.find_elements_by_xpath("/html/body/div/div/div/div/main/div[3]/div[3]/div/div[2]/ul/li")[-1].find_element_by_xpath("div/span/a").click()

