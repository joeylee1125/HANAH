# -*- coding: UTF-8 -*-
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

import unittest
import time

class GetWenshu():
    def __init__(self):
        self.url = "http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+1+AJLX++案件类型:刑事案件"

    def open(self):
        self.driver = webdriver.Chrome(executable_path=r"C:\webdriver\chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(self.url)

    def quit(self):
        self.driver.quit()

    def check_select_all(self):
        driver = self.driver
        check_all = WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_name("ckall"))
        check_all.click()


    def download_all(self):
        driver = self.driver
        batch_download_button = WebDriverWait(driver, 60).until(lambda driver: driver.find_elements_by_class_name("list-operate"))
        batch_download_button[1].click()

    def select_20_items_per_page(self):
        print("Select 20 itmes per page.")
        driver = self.driver
        dropdown_button = WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath("//div[@class='pageNumber']/div[2]/div/table/tbody/tr/td[2]/input"))
        print("Try to click dropdown list")
        dropdown_button.click()

        print("Try to select 20")
        #s = WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath("//div[@class='pageNumber']/div[2]/div/div/ul/li[4]"))
        s = WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath("//div[@class='pageNumber']/div[2]/div"))

        s.click()
        #Select(s).select_by_value("20")
        #print(Select(s).all_selected_options)

def test():
    ws_page = GetWenshu()
    ws_page.open()
    ws_page.select_20_items_per_page()
    time.sleep(60)
    #ws_page.check_select_all()
    # ws_page.download_all()


def main():
    test()


if __name__ == '__main__':
    main()