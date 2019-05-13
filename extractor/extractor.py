import requests
import time

body_request = {
            "url": "https://www.magazineluiza.com.br/smartphone-samsung-galaxy-j4-core-tela-infinita-de-6-camera-frontal-de-5mp-android-go-8-1-preto-/p/djkg14gfcc/te/sj4c/",
            "max_number": 1,
            "similar_products_container_tag": "div",
            "similar_products_container_class": "slick-track",
            "data": [{
              "name": "price",
              "container_tag": "div",
              "container_class": "price-template",
              "to_get": "text",
              "required": True
            }],
            "blacklist": [],
            "sleep_time": 20
        }

all_data = list()


def extract(number_of_items=3):
    while True:
        response = requests.post('http://localhost:5000/mine', json=body_request)
        if response.content != 'tasks already running, try again later':
            task_id = response.content
            request = requests.get('http://localhost:5000/mine', params={'job_id': task_id.decode("utf-8")})
            while 'content' not in request.json():
                request = requests.get('http://localhost:5000/mine', params={'job_id': task_id.decode("utf-8")})
                print(request.json())
                time.sleep(20)
            data = request.json()
            all_data.extend(data['content']['content'])
            body_request['url'] = data['content']['last_url']
            body_request['blacklist'] = [item['title'] for item in all_data]
            if len(all_data) == number_of_items:
                print(all_data)
                break


if __name__ == '__main__':
    extract()