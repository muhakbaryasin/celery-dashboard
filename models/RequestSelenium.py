from models.WebDriver import WebDriver
from selenium.webdriver.common.keys import Keys


def run():
    wd = WebDriver('http://www.python.org')
    assert "Python" in wd.session.title
    elem = wd.findElementByName("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    h3_elem = wd.session.find_element_by_xpath('//*[@id="content"]/div/section/form/ul/li[1]/h3/a')
    print(h3_elem.text)
    assert "No results found." not in wd.session.page_source

