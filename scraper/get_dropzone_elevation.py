from selenium import webdriver

driver = webdriver.Chrome()
url = "https://wingsuit.world/dropzones/"

table_XPath = '//tbody/'

driver.get(url)
number_of_entries = driver.find_element(by='xpath', value="//div[@id='tablepress-14_info']").text
assert "241 entries" in number_of_entries
print(number_of_entries)