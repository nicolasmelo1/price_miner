import requests
from logging import Logger
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os


def test():
    driver = webdriver.Remote(command_executor=' http://172.20.0.2:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
    driver.get("https://www.americanas.com.br/produto/132381423/notebook-lenovo-2-em-1-yoga-520-intel-core-i7-8gb-1tb-tela-14-windows-10-platinum?DCSext.recom=RR_item_page.rr1-ClickCP&nm_origem=rec_item_page.rr1-ClickCP&nm_ranking_rec=13")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "lxml")
    print(soup.find("div", class_="main-price").text)
    next_item = soup.find("div", class_="slick-track")
    next_link = [a['href'] for a in next_item.find_all("a", href=True)]
    driver.quit()

