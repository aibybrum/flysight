from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://wingsuit.world/dropzones/")

l = driver.find_elements_by_xpath ("//*[@class= 'dataTable']/tbody/tr")
print(len(l)) 
driver.quit()