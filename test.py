from webtest import TestApp
from main import app as wsgi_app
import json

app = TestApp(wsgi_app)


def test_requests():
    resp = app.get('/letter')
    assert 'guest' in resp.json['userList']
    user_info = dict(username='guest2', password='guest2', name='Guest')
    resp = app.post('/users.json', content_type='application/json', body=json.dumps(user_info)
    assert resp.json == user_info












# import httplib2
#
# httplib2.debuglevel = 1
#
# h = httplib2.Http()
#
# url = 'http://127.0.0.1:8000/letter'
# data = ("2", ((2.1, {'col1': 1, 'col2': 2}), (2.2, {'col1': 3, 'col2': 4})))
# headers = {'Content-Type': 'application/json'}
# resp, content = h.request(url, 'POST', json.dumps(data), headers)
# print(resp, content)
#
# url = 'http://127.0.0.1:8000/pile'
# resp, content = h.request(url, 'GET')
# print(resp, '\n', content)
#
# url = 'http://127.0.0.1:8000/letter/remove/2'
# resp, content = h.request(url, 'DELETE')
# print(resp, '\n', content)
#
# url = 'http://127.0.0.1:8000/pile'
# resp, content = h.request(url, 'GET')
# print(resp, '\n', content)
