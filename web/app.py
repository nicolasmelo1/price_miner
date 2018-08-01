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
    data = request.get_json()
    task = celery.send_task('mine', kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(id=task.id,
                url=url_for('check_task', id=task.id, _external=True))


@app.route('/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    if res.state==states.PENDING:
        return res.state
    else:
        return jsonify(
            task_id=res.id,
            content=res.result
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0')