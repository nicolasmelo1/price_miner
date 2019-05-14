from app import celery, SELENIUM_WEBDRIVER_HOST
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import randint


def find_next_url(next_links_container_content, links, main_url):
    if next_links_container_content:
        possible_next_links = [a['href'] for a in next_links_container_content.find_all("a", href=True)]
        if main_url:
            next_link = main_url + possible_next_links[randint(0, len(possible_next_links) - 1)]
            links.append(next_link)
            url = next_link
        else:
            next_link = possible_next_links[randint(0, len(possible_next_links) - 1)]
            links.append(next_link)
            url = next_link
    else:
        url = links[randint(0, len(links) - 1)]
    return url, links


@celery.task(name='ping', bind=True)
def ping(self, **kwargs):
    return 'pong'


@celery.task(name='handle_request', bind=True, max_retries=5)
def handle_request(self, url, max_number, similar_products_container_tag, similar_products_container_class,
                   response, response_data, whitelist, blacklist, main_url, sleep_time, links, *args, **kwargs):
    driver = webdriver.Remote(command_executor=SELENIUM_WEBDRIVER_HOST,
                              desired_capabilities=DesiredCapabilities.FIREFOX)
    try:
        driver.get(url)
        time.sleep(sleep_time)
        soup = BeautifulSoup(driver.page_source, "lxml")
        next_links_container_content = soup.find(similar_products_container_tag,
                                                 class_=similar_products_container_class)
        url, links = find_next_url(next_links_container_content, links, main_url)
        if any([d for d in response['content'] if soup.title.text in d.get('title', None)]):
            driver.quit()
            return url, links, response, 'Title already exists or price container doesn\'t exist for url'
        elif whitelist or blacklist:
            if whitelist and not any([item.lower() in soup.title.text.lower() for item in whitelist]):
                driver.quit()
                return url, links, response, 'The item title does not contain one of the following types: %s' \
                                                   % ','.join(whitelist)
            if blacklist and any([item.lower() in soup.title.text.lower() for item in blacklist]):
                driver.quit()
                return url, links, response, 'The item title does contain one of the following types: %s' \
                       % ','.join(blacklist)

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
            driver.quit()
            return url, links, response, 'One or more required data could not be extracted'
        else:
            response['content'].append(item_data)
            driver.quit()
            return url, links, response, 'item extracted successfully'
    except Exception as e:
        driver.quit()
        raise self.retry(countdown=60, exc=e)


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
    max_number = 5 if max_number > 45 else max_number
    sleep_time = 10 if sleep_time > 60 else sleep_time
    links = list()

    response = {
        'last_url': '',
        'content': [],
    }
    self.update_state(state='EXTRACTING', meta={
        'job_percent_completed': len(response['content']) / max_number,
        'current_url': url
    })
    while True:
        handle_request_response = handle_request.delay(url, max_number,
                                                       similar_products_container_tag,
                                                       similar_products_container_class,
                                                       response, response_data, whitelist, blacklist,
                                                       main_url, sleep_time, links)

        while not handle_request_response.ready():
            time.sleep(5)

        if handle_request_response.state == 'SUCCESS':
            url, links, response, message = handle_request_response.result
            self.update_state(state='EXTRACTING', meta={
                'job_percent_completed': len(response['content'])/max_number,
                'current_url': url,
                'message': message,
                'Errors': None
            })
        elif handle_request_response.state == 'FAILURE':
            response['last_url'] = url
            break

        if len(response['content']) == max_number:
            response['last_url'] = url
            break

    return response
