from selenium import webdriver
from selenium.webdriver.common.by import By
option=webdriver.ChromeOptions()
option.add_experimental_option(name="detach", value=True)
instance=webdriver.Chrome(options=option)
instance.get("http://python.org")
dates=instance.find_elements(By.CSS_SELECTOR, value=".event-widget .menu time")
titles=instance.find_elements(By.CSS_SELECTOR, value=".event-widget .menu a")
#print(len(title))
#print(date.text)
# with comprehention dictionary and range
#events= {i:{'time':date[i].text, 'name':title[i].text} for i in range(len(date))}
# with range and index on the lists
'''for i in range(len(date)):
    events[i]={
        'time':date[i].text, 
        'name':title[i].text
    }'''
# with zip function
events=dict()
for date, title in zip(dates,titles):
    events[dates.index(date)]={'date':date.text, 'name':title.text}
# print the result
print(events)
instance.quit()
