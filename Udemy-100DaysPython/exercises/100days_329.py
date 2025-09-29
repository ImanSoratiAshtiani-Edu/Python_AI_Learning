from bs4 import BeautifulSoup as bs
with open("C:\\Users\\imana\\Documents\\Courses\\Udemy\\py100\\bs4-start\\website.html") as file:
    soup=bs(file, "html.parser")
    #print(soup.prettify())
    #print(soup.title)
    #print(soup.title.string)
    #print(soup.title.text)
    #print(soup.title.getText())
    #print(soup.title.name)
    ## 3 mode of find the first occurance of an anchor element
    #print(soup.a)
    #print(soup.find("a"))
    #print(soup.select_one("a"))
    ## 3 mode for retrieve the text between opening and closing anchor:
        ### instead of soup.a. you can use any of the above mode
    #print(soup.a.string)
    #print(soup.a.text)
    #print(soup.a.getText())
    ## 2 modes to get the attribute of an anchor element:
    #print(soup.a.get("href")) #TypeError: 'NoneType' object is not callable
    #print(soup.a["href"])
    ## 3 modes to find all occurance of an anchor element as a list:
    #print(soup.find_all("a"))
    #print(soup("a"))  equivalent of print(soup.find_all("a"))
    #print(soup.select("a"))
    ## the only mode to get an anchor element with the structure:
    #print(soup.find_all("p a")) # []---it doesn't work!!!
    #print(soup.select("p a")) # [<a href="https://www.appbrewery.co/">The App Brewery</a>]
    ## 2 modes to retrieve the text, attribute ecc for all occurance of an anchor element:
    '''
    for occ in soup.select("a"):
        print(occ.text)
        print(occ["href"])
        print(occ.get("href"))
    '''
    '''
    for occ in soup.find_all("a"):
        print(occ.text)
        print(occ.get("href"))
        print(occ["href"])
    '''
    print([(el.text,el["href"]) for el in soup("a")])