from app import celery, SELENIUM_WEBDRIVER_HOST
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import randint


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


@celery.task(name='ping', bind=True)
def ping(self, **kwargs):
    return 'pong'


@celery.task(name='mine', bind=True)
def mine(self, data, *args, **kwargs):
    url = data['url']
    max_number = data['max_number']
    similar_products_container_tag = data['similar_products_container_tag']
    similar_products_container_class = data['similar_products_container_class']
    response_data = data['data']
    whitelist = data.get('whitelist', [])
    blacklist = data.get('blacklist', [])
    main_url = data.get('main_url', None)
    sleep_time = data.get('sleep_time', 5)
    max_number = 5 if max_number > 85 else max_number
    sleep_time = 10 if sleep_time > 60 else sleep_time
    driver = webdriver.Remote(command_executor=SELENIUM_WEBDRIVER_HOST, desired_capabilities=DesiredCapabilities.FIREFOX)
    links = list()

    response = {
        'last_url': '',
        'content': [],
        'error': '',
    }

    while True:
        try:
            driver.get(url)
            time.sleep(sleep_time)
            soup = BeautifulSoup(driver.page_source, "lxml")
            if any([d for d in response['content'] if soup.title.text in d.get('title', None)]):
                next_links_container_content = soup.find(similar_products_container_tag,
                                                         class_=similar_products_container_class)
                url, links = find_next_url(next_links_container_content, links, main_url)
                self.update_state(state='EXTRACTING', meta={
                    'job_percent_completed': len(response['content'])/max_number,
                    'job_current_status': 'Title already exists or price container doesn\'t exist for url',
                    'current_url': url,
                    'Errors': None
                })
                continue
            elif whitelist or blacklist:
                if not any(item.lower() in soup.title.text.lower() for item in whitelist):
                    url = links[randint(0, len(links) - 1)]
                    self.update_state(state='EXTRACTING', meta={
                        'job_percent_completed': len(response['content']) / max_number,
                        'job_current_status':
                            'The item title does not contain one of the following types: %s' % ','.join(whitelist),
                        'current_url': url,
                        'Errors': None
                    })
                    continue
                elif any(item.lower() in soup.title.text.lower() for item in blacklist):
                    url = links[randint(0, len(links) - 1)]
                    self.update_state(state='EXTRACTING', meta={
                        'job_percent_completed': len(response['content']) / max_number,
                        'job_current_status':
                            'The item title does contain one of the following types: %s' % ','.join(blacklist),
                        'current_url': url,
                        'Errors': None
                    })
                    continue
                else:
                    pass
            item_data = {
                "title": soup.title.text,
                "data": {}
            }
            set_loop_as_error = False
            for to_extract in response_data:
                default_to_extract = soup.find(to_extract['container_tag'], class_=to_extract['container_class'])
                if default_to_extract:
                    if 'to_get' not in to_extract or to_extract['to_get'] == 'text':
                        item_data['data'][to_extract['name']] = default_to_extract.text
                    else:
                        item_data['data'][to_extract['name']] = default_to_extract[to_extract['to_get']]
                elif to_extract['required']:
                    set_loop_as_error = True
                    break
                else:
                    item_data['data'][to_extract['name']] = ''
            if set_loop_as_error:
                next_links_container_content = soup.find(similar_products_container_tag,
                                                         class_=similar_products_container_class)
                url, links = find_next_url(next_links_container_content, links, main_url)
                self.update_state(state='EXTRACTING', meta={
                    'job_percent_completed': len(response['content']) / max_number,
                    'job_current_status':
                        'One or more required data could not be extracted',
                    'current_url': url,
                    'Errors': None
                })
                continue
            else:
                response['content'].append(item_data)
            next_links_container_content = soup.find(similar_products_container_tag,
                                                     class_=similar_products_container_class)
            if len(response['content']) == max_number:
                response['last_url'] = url
                driver.quit()
                break
            self.update_state(state='EXTRACTING', meta={
                'job_percent_completed': len(response['content']) / max_number,
                'job_current_status': 'Item extracted successfully',
                'current_url': url,
                'Errors': None
            })
            url, links = find_next_url(next_links_container_content, links, main_url)
        except Exception as e:
            response['last_url'] = url
            response['error'] = str(e)
            driver.quit()
            break
    return response
