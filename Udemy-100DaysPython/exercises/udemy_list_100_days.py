
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import time
url="C:/Users/imana/Documents/Courses/Udemy/Course.mhtml"
with open(url) as file:
    file_content = file.read()
    content= bs(file_content, "html.parser")
    #print(content.get_text())
    li=content.find_all("h3")
    for i in li:
        print(i.get_text().replace("=\n","").split(":"))
with open("C:/Users/imana/Documents/Courses/Udemy/course_sections.txt",'w') as section:
    for i in li:
        print(i.get_text().replace("=\n","").split(":"),file=section)

