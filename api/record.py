from bottle import request, response
from bottle import post, get, put, delete
import re
import json
from data import record


@get('/paper/<stamp>/record/<signet>')
def listing_handler(stamp, signet):
    """Handles name listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'record': record.get_record(stamp, signet)})


@put('/pile/paper/<signet>')
def update_handler(record):
    """Handles name updates"""
    pass