from bottle import request, response
from bottle import post, get, put, delete
import re
import json
from data import pile, letter


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