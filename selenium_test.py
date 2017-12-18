# -*- coding: UTF-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\webdriver\chromedriver.exe")

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found" not in driver.page_source

    def tearDown(self):
        self.driver.quit()


TIMEOUT = 180

def get_chrome_driver():
    print('Try to get chrome driver.')
    # chromedriver
    driver = None
    try:
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path=r"C:\webdriver\chromedriver.exe", chrome_options=options)

        # 设置超时时间
        driver.set_page_load_timeout(TIMEOUT)
        driver.set_script_timeout(TIMEOUT)  # 这两种设置都进行才有效
    except Exception as e:
        print("get_chrome_driver() Exception: %s" % e)
        if driver:
            driver.quit()
        return None
    else:
        return driver

def open_page():
    driver = None
    try:
        driver = get_chrome_driver()
        if not driver:
            print("no driver found")
            return ""
        print('Open a page')
        driver.get("http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件")
        driver.implicitly_wait(20)
        driver.maximize_window()
        #driver.get(\
        #"http://wenshu.court.gov.cn/list/list/?sorttype=1&\
        #conditions=searchWord+1+AJLX++案件类型:刑事案件&\
        #conditions=searchWord+四川省+++法院地域:四川省&\
        #conditions=searchWord+2014+++裁判年份:2014")
        #id = driver.find_elements_by_xpath('//*[@class]')
        #for i in id:
        #    print(i.get_attribute('class'))
        #//*[@id="operate"]/div[2]/span
        #
        #download_button = driver.find_elements_by_link_text('批量下载')
        #print(download_button)
        batch_download_checkbox = driver.find_element_by_name("ckall")
        batch_download_checkbox.click()
        batch_download_button = driver.find_elements_by_class_name("list-operate")
        #total_item = driver.find_element_by_id("span_datacount").text
        #print(total_item)
        #batch_download_button = driver.find_element_by_xpath("//span[text()='批量下载']")
        #batch_download_button.click()
    except Exception as e:
        print("Exception: %s" % e)
        return ""
    else:
        print("")
    #finally:
    #    if driver:
    #        driver.quit()        
        
def test():
    driver = webdriver.Chrome(executable_path=r"C:\webdriver\chromedriver.exe")
    driver.set_page_load_timeout(120)
    driver.get("http://www.google.com")
    driver.maximize_window()
    driver.implicitly_wait(20)
    driver.quit()
    
def main():
    #get_chrome_driver()
    open_page()
    #test()

if __name__ == '__main__':
    main()
    #unittest.main()