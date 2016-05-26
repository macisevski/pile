import json

from bottle import get
from bottle import response

from data import pile


@get('/pile')
def listing_handler():
    """Handles name listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(pile.list())
