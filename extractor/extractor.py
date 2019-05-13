from argparse import ArgumentParser
import requests
import time

price_miner_host = "https://price-miner.herokuapp.com"

body_request = {
    "url": "https://www.magazineluiza.com.br/iphone-8-apple-64gb-dourado-4g-tela-47-retina-cam-12mp-selfie-7mp-ios-11/p/155542800/te/teip/",
    "max_number": 30,
    "similar_products_container_tag": "ul",
    "similar_products_container_class": "showcase showcase__five-product js-carousel-showcase-wvav slick-initialized slick-slider",
    "data": [{
      "name": "price",
      "container_tag": "div",
      "container_class": "price-template",
      "to_get": "text",
      "required": True
    }],
    "blacklist": [],
    "whitelist": ["smartphone", "samsung", "xiaomi", "android", "iphone", "apple"],
    "sleep_time": 20
}

all_data = list()


def extract(number_of_items=1):
    while True:
        response = requests.post(price_miner_host + '/mine', json=body_request)
        if response.content != 'tasks already running, try again later':
            task_id = response.content
            request = requests.get(price_miner_host + '/mine', params={'job_id': task_id.decode("utf-8")})
            while 'content' not in request.json():
                request = requests.get(price_miner_host + '/mine', params={'job_id': task_id.decode("utf-8")})
                print(request.json())
                time.sleep(20)
            data = request.json()
            all_data.extend(data['content']['content'])
            body_request['url'] = data['content']['last_url']
            body_request['blacklist'] = [item['title'] for item in all_data]
            if len(all_data) >= number_of_items:
                print(all_data)
                break


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--num', required=False, type=int, help='number of items to extract')
    args = parser.parse_args()
    if args:
        extract(args.num)
    else:
        extract()
