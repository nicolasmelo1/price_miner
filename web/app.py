from flask import Flask, jsonify, url_for
import celery.states as states
from worker import celery
from flask import request

app = Flask(__name__)


@app.route('/')
def application_status():
    return 'Application Up'


@app.route('/mine', methods=['GET', 'POST'])
def mine():
    """
    Sends async run to celery to get data from e-commerce websites.

    If POST:
    JSON - Parameters
    -----------------------
    url (String): Initial url from e-commerce to extract data from.
    max_number (Integer): max number of items to extract from e-commerce.
    similar_products_container_tag (String): The container for similar products (div, ul, etc.).
    similar_products_container_class (String): The class of the container for similar products.
    price_container_tag (String): The container to get products price (div, ul, etc.).
    price_container_class (String): The class of the container to get products price.
    OPTIONAL main_url (String): The main url of the website.
    :return: Celery task id

    If GET:
    Parameters
    -----------------------
    job_id (String): The id of celery task
    if Job Running:
        :return: The task state
    If Job Completed
        :return: JSON with task id and task result
    """

    if request.method == 'POST':
        data = request.get_json()
        task = celery.send_task('mine', kwargs=data)
        return task.id
    if request.method == 'GET':
        request.args.get('job_id')
        res = celery.AsyncResult(id)
        if res.state == 'PENDING':
            return res.state
        else:
            return jsonify(
                task_id=res.id,
                content=res.result
            )


if __name__ == '__main__':
    app.run(host='0.0.0.0')