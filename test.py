import httplib2
h = httplib2.Http('.cache')
response, content = h.request('http://127.0.0.1:8000/pile')
print(content)
response, content = h.request('http://127.0.0.1:8000/paper/1')
print(content)
response, content = h.request('http://127.0.0.1:8000/paper/1/record/1')
print(content)