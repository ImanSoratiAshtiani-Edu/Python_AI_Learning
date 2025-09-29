from selenium import webdriver
from selenium.webdriver.common.by import By
# keep chrome browser open after program finishes
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
# create an instance and open a website
driver = webdriver.Chrome(options=chrome_options)
URL="https://www.amazon.it/OMEGA-KRILL-OIL-Salugea-assimilabili/dp/B07QW876R7/ref=pd_rhf_gw_s_bmx_gp_oi7yiu4o_d_sccl_1_2/262-0217613-0324745?pd_rd_w=6P2nz&content-id=amzn1.sym.97f33c67-c843-4129-9054-54f7390b5c5d&pf_rd_p=97f33c67-c843-4129-9054-54f7390b5c5d&pf_rd_r=KSPS5Q0JR376XK5ZXJJJ&pd_rd_wg=2NR59&pd_rd_r=411f0020-1672-4a84-a4f1-8a98394e96f1&pd_rd_i=B07QW876R7&psc=1"
driver.get(URL)
# find elements of price
price_whole=driver.find_element(By.CLASS_NAME,value="a-price-whole")
price_fraction=driver.find_element(By.CLASS_NAME,"a-price-fraction")
# print the price
print(f"The price is {price_whole.text}.{price_fraction.text} €")
#driver.close() # close a single tab of a particular page
driver.quit() # quit the entire browser


