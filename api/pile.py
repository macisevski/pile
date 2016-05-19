from bottle import request, response
from bottle import get, put, delete
import re
import json
from data import pile


@get('/pile')
def listing_handler():
    """Handles name listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'pll': pile.get_pile()})
