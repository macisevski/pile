import json

from bottle import get, put
from bottle import response

from data import pile


@get('/paper/<stamp>/record/<signet>')
def listing_handler(stamp, signet):
    """Handles name listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    _letter = pile.get_letter(stamp)
    return json.dumps({'record': _letter.get_line(signet)})


@put('/pll/paper/<signet>')
def update_handler(line):
    """Handles name updates"""
    pass