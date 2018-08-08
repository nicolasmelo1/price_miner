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
    if main_url:
        next_link = main_url + possible_next_links[randint(0, len(possible_next_links) - 1)]
        links.append(next_link)
        url = next_link
    else:
        next_link = possible_next_links[randint(0, len(possible_next_links) - 1)]
        links.append(next_link)
        url = next_link
    return url, links


@celery.task(name='mine', bind=True)
def mine(self, **kwargs):
    url = kwargs['url']
    max_number = kwargs['max_number']
    similar_products_container_tag = kwargs['similar_products_container_tag']
    similar_products_container_class = kwargs['similar_products_container_class']
    price_container_tag = kwargs['price_container_tag']
    price_container_class = kwargs['price_container_class']
    main_url = kwargs.get('main_url', None)
    item_types = kwargs.get('item_types', [])
    sleep_time = kwargs.get('sleep_time', 5)
    max_number = 5 if max_number > 85 else max_number
    sleep_time = 5 if sleep_time > 60 else sleep_time
    driver = webdriver.Remote(command_executor='selenium-hub:4444/wd/hub',
                              desired_capabilities=DesiredCapabilities.CHROME)
    links = list()
    content = list()
    while True:
        try:
            driver.get(url)
            time.sleep(sleep_time)
            soup = BeautifulSoup(driver.page_source, "lxml")
            if not soup.find("div", class_="price-template") or\
                    any([d for d in content if soup.title.text in d.get('title', None)]):
                next_links_container_content = soup.find(similar_products_container_tag,
                                                         class_=similar_products_container_class)
                url, links = find_next_url(next_links_container_content, links, main_url)
                self.update_state(state='EXTRACTING', meta={
                    'job_percent_completed': len(content)/max_number,
                    'job_current_status': 'Title already exists or price container doesn\'t exist for url',
                    'current_url': url,
                    'Errors': None
                })
                continue
            elif item_types:
                if any(item.lower() in soup.title.text.lower() for item in item_types):
                    url = links[randint(0, len(links) - 1)]
                    self.update_state(state='EXTRACTING', meta={
                        'job_percent_completed': len(content) / max_number,
                        'job_current_status':
                            'The item title does not contain one of the following types: %s' % ','.join(item_types),
                        'current_url': url,
                        'Errors': None
                    })
                    continue

                else:
                    pass
            data = {
                "title": soup.title.text,
                "data": soup.find(price_container_tag, class_=price_container_class).text
            }
            content.append(data)
            next_links_container_content = soup.find(similar_products_container_tag,
                                                     class_=similar_products_container_class)
            if len(content) == max_number:
                driver.quit()
                break
            self.update_state(state='EXTRACTING', meta={
                'job_percent_completed': len(content) / max_number,
                'job_current_status': 'Item extracted successfully',
                'current_url': url,
                'Errors': None
            })
            url, links = find_next_url(next_links_container_content, links, main_url)
        except Exception as e:
            print("[ERROR]: Error when trying to get url: %s with error: %s" % (url, str(e)))
            driver.quit()
            driver = webdriver.Remote(command_executor='selenium-hub:4444/wd/hub',
                                      desired_capabilities=DesiredCapabilities.CHROME)
            self.update_state(state='EXTRACTING', meta={
                'job_percent_completed': len(content) / max_number,
                'job_current_status': 'Unexpected Error',
                'current_url': url,
                'Errors': str(e)
            })
            url = links[randint(0, len(links)-1)]

    return content
