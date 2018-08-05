from celery import Celery
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import randint

celery = Celery('tasks',
                broker='redis://redis:6379/0',
                backend='redis://redis:6379/0')


def find_next_url(next_links_container_content, links, main_url):
    possible_next_links = [a['href'] for a in next_links_container_content.find_all("a", href=True)]
    print(possible_next_links)
    if main_url:
        next_link = main_url + possible_next_links[randint(0, len(possible_next_links) - 1)]
        links.append(next_link)
        url = next_link
    else:
        next_link = possible_next_links[randint(0, len(possible_next_links) - 1)]
        links.append(next_link)
        url = next_link
    return url, links


@celery.task(name='mine')
def mine(**kwargs):
    url = kwargs['url']
    max_number = kwargs['max_number']
    similar_products_container_tag = kwargs['similar_products_container_tag']
    similar_products_container_class = kwargs['similar_products_container_class']
    price_container_tag = kwargs['price_container_tag']
    price_container_class = kwargs['price_container_class']
    main_url = kwargs.get('main_url', None)

    driver = webdriver.Remote(command_executor='selenium-hub:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.FIREFOX)
    links = list()
    content = list()
    while True:
        try:
            driver.get(url)
        except Exception as e:
            print("[Error] failed to get data from url: %s" % url)
            url = links[randint(0, len(links) - 1)]
            continue
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "lxml")
        if any([d for d in content if soup.title.text in d.get('title', None)]):
            next_links_container_content = soup.find(similar_products_container_tag,
                                                     class_=similar_products_container_class)
            url, links = find_next_url(next_links_container_content, links, main_url)
            continue
        elif 'notebook' not in soup.title.text.lower():
            url = links[randint(0, len(links) - 1)]
            continue
        data = {
            "title": soup.title.text,
            "data": soup.find(price_container_tag, class_=price_container_class).text
        }
        content.append(data)
        next_links_container_content = soup.find(similar_products_container_tag, class_=similar_products_container_class)
        if len(content) == max_number:
            break
        try:
            url, links = find_next_url(next_links_container_content, links, main_url)
            pass
        except Exception as e:
            print("error is: " + str(e))
            driver = webdriver.Remote(command_executor='selenium-hub:4444/wd/hub',
                                      desired_capabilities=DesiredCapabilities.FIREFOX)
            url = links[randint(0, len(links)-1)]
    return content
