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
    '''
    :return: task_id
    '''
    if request.method == 'POST':
        data = request.get_json()
        task = celery.send_task('mine', kwargs=data)
        return task.id


@app.route('/check/<string:id>')
def check_task(id):
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