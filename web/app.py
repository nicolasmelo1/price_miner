from flask import Flask, jsonify, url_for
import celery.states as states
from worker import celery


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/mine')
def test():
    task = celery.send_task('mine', kwargs={})
    return "<a href='{url}'>check status of {id} </a>".format(id=task.id,
                url=url_for('check_task',id=task.id,_external=True))

@app.route('/check/<string:id>')
def check_task(id):
    res = celery.AsyncResult(id)
    if res.state==states.PENDING:
        return res.state
    else:
        return str(res.result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')