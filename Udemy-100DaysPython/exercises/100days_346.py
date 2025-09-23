
from selenium import webdriver
from selenium.webdriver.common.by import By
URL="https://www.python.org/"

chrome_option=webdriver.ChromeOptions()
chrome_option.add_experimental_option(name="detach",value=True)
driver=webdriver.Chrome(options=chrome_option)
driver.get(URL)
search_bar=driver.find_element(By.NAME,value="q") # very useful for the forms
print(search_bar)
print(search_bar.tag_name)
print(search_bar.get_attribute("placeholder"))

button=driver.find_element(By.ID,value="submit")
print(button.size)
documentation_link=driver.find_element(By.CSS_SELECTOR,value=".documentation-widget a")
print(documentation_link.text)
print(documentation_link.get_attribute("href"))

python_books=driver.find_element(By.XPATH,value='//*[@id="container"]/li[3]/ul/li[8]/a')
print(python_books.text)
driver.get(python_books.get_attribute("href"))

#driver.quit() # quit the entire browser