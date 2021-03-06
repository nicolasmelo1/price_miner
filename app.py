from flask import Flask, jsonify
from flask import request
from worker import make_celery
import os


app = Flask(__name__)

if os.environ.get('FLASK_ENV') == 'development':
    CELERY_BROKER_URL = 'redis://redis:6379'
    CELERY_RESULT_BACKEND = 'redis://redis:6379'
    SELENIUM_WEBDRIVER_HOST = 'http://seleniumhub:4444/wd/hub'
else:
    CELERY_BROKER_URL = os.environ.get("REDIS_URL")
    CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")
    SELENIUM_WEBDRIVER_HOST = "price-miner-selenium.herokuapp.com/wd/hub"

app.config.update(
    CELERY_BROKER_URL=CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND=CELERY_RESULT_BACKEND
)
celery = make_celery(app)


from tasks import tasks


@app.route('/')
def application_status():
    return 'Application Up'


@app.route('/ping')
def ping():
    result = tasks.ping.delay()
    result.wait()
    return result.get()


@app.route('/mine', methods=['GET', 'POST'])
def mine():
    """
    Sends async run to celery to get data from e-commerce websites.

    If POST: (If tasks are running send message)
    JSON - Parameters
    -----------------------
    url (String): Initial url from e-commerce to extract data from.
    max_number (Integer): max number of items to extract from e-commerce.
    similar_products_container_tag (String): The container for similar products (div, ul, etc.).
    similar_products_container_class (String): The class of the container for similar products.
    price_container_tag (String): The container to get products price (div, ul, etc.).
    price_container_class (String): The class of the container to get products price.
    OPTIONAL whitelist (List[String]): Tells what string the title can contain. Ex.: If you only
                                        want to retrieve notebooks you would send a list ['notebook']
                                        if you want monitors also would be ['notebook', 'monitor']
    OPTIONAL blacklist (List[String]): Tells what string the title CANNOT contain. Ex.: If you DON￿'T
                                        want to retrieve notebooks you would send a list ['notebook']
                                        if you DON￿'T want monitors also, it would be ['notebook', 'monitor']
    OPTIONAL sleep_time (Integer): Max time to sleep until retrieve data. Default: 5
    OPTIONAL main_url (String): The main url of the website.
    :return: Celery task id

    If GET:
    Parameters
    -----------------------
    job_id (String): The id of celery task
    if Job Running:
        :return: The task state
    If Job Completed:
        :return: JSON with task id and task result
    """

    if request.method == 'POST':
        required_fields = ['url', 'max_number', 'similar_products_container_tag',
                          'similar_products_container_class', 'data']
        data = request.get_json()
        if [i for i in required_fields if i in list(data.keys())] == required_fields:
            i = celery.control.inspect()
            active_tasks = i.active()
            active_mine_tasks = [item['name'] for item in list(active_tasks.values())[0]]
            if active_mine_tasks.count('mine') > 0:
                return 'tasks already running, try again later'
            task = tasks.mine.delay(data)
            return task.id
        else:
            return 'Parece que a informação passada não está no formato certo'
    if request.method == 'GET':
        job_id = request.args.get('job_id')
        res = celery.AsyncResult(job_id)

        if res.state == 'PENDING':
            return jsonify(
                task_id=res.id,
                status=res.state,
            )
        elif res.state == 'EXTRACTING':
            return jsonify(
                task_id=res.id,
                status=res.state,
                data=res.result
            )
        elif res.state == 'SUCCESS':
            return jsonify(
                task_id=res.id,
                status=res.state,
                content=res.result
            )
        else:
            return jsonify(
                task_id=res.id,
                status=res.state
            )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
