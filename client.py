import httplib2
import json

httplib2.debuglevel = 1

h = httplib2.Http()

url = 'http://127.0.0.1:8000/letter'
data = ("2", ((2.1, {'col1': 1, 'col2': 2}), (2.2, {'col1': 3, 'col2': 4})))
headers = {'Content-Type': 'application/json'}
resp, content = h.request(url, 'POST', json.dumps(data), headers)
print(resp, content)

url = 'http://127.0.0.1:8000/pile'
resp, content = h.request(url, 'GET')
print(resp, '\n', content)

url = 'http://127.0.0.1:8000/letter/remove/2'
resp, content = h.request(url, 'DELETE')
print(resp, '\n', content)

url = 'http://127.0.0.1:8000/pile'
resp, content = h.request(url, 'GET')
print(resp, '\n', content)
