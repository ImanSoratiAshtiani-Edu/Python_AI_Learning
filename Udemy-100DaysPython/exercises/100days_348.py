# interaction.py
from fontTools.subset.svg import xpath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from trio import sleep

option=webdriver.ChromeOptions()
option.add_experimental_option(name="detach", value=True)
instance=webdriver.Chrome(options=option)
instance.get("https://en.wikipedia.org/wiki/Main_Page")
# we can use three solutions
statistics=instance.find_elements(By.CSS_SELECTOR,value="#articlecount li a")[1]
print(statistics.text)
statistics=instance.find_elements(By.CSS_SELECTOR,value="#articlecount a")[1] # li is not necessary here
print(statistics.text)
statistics=instance.find_element(By.XPATH, value='//*[@id="articlecount"]/ul/li[2]/a[1]')
print(statistics.text)
#statistics.click()
element = instance.find_element(By.LINK_TEXT, value= "Spaceship House")
#element.click()
search_text=instance.find_element(By.NAME, value="search")
instance.maximize_window()
search_text.send_keys("Python", Keys.ENTER )
#instance.quit()