from argparse import ArgumentParser
from config import PRICE_MINER_HOST, BODY_REQUEST
from json.decoder import JSONDecodeError
import requests
import time
import pandas as pd

all_data = list()


def extract(number_of_items=1):
    while True:
        response = requests.post(PRICE_MINER_HOST + '/mine', json=BODY_REQUEST)
        if response.content != 'tasks already running, try again later':
            task_id = response.content
            while True:
                request = requests.get(PRICE_MINER_HOST + '/mine', params={'job_id': task_id.decode("utf-8")})
                if request.status_code == 200 and 'content' in request.json():
                    break
                time.sleep(20)
            data = request.json()
            all_data.extend(data['content']['content'])
            BODY_REQUEST['url'] = data['content']['last_url']
            BODY_REQUEST['blacklist'] = [item['title'] for item in all_data]
            if len(all_data) >= number_of_items:
                data_holder = list()
                for item in all_data:
                    temp = {'title': item['title']}
                    for key, value in item['data'].items():
                        temp[key] = value
                    data_holder.append(temp)
                pd.DataFrame.from_dict(data, orient='index', columns=['title', 'price']).to_csv('magalu_data.csv')
                break


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--num', required=False, type=int, help='number of items to extract')
    args = parser.parse_args()
    if args:
        extract(args.num)
    else:
        extract()
