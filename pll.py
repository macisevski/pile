"""
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
"""

import json
import re
import unittest
import tempfile
from unittest import mock
from random import choice, randint
from string import ascii_letters, digits

import bottle
from bottle import post, get, put, delete
from bottle import request, response
from unqlite import UnQLite
from webtest import TestApp


###############################################################################
# Model ########################################################################
###############################################################################

class Pile:
    def __init__(self, db):
        self.db = db

    def list(self):
        return [item for item in self.db]

    def find(self, stamp):
        try:
            return self.db[stamp]
        except KeyError:
            raise

    def add(self, stamp, letter):
        if not self.db.exists(stamp):
            self.db[stamp] = letter
        else:
            raise KeyError
        return self.find(stamp)

    def bin(self, stamp):
        try:
            self.db.delete(stamp)
        except KeyError:
            raise


class Letter:
    def get_line(letter, signet):
        try:
            line = letter[signet]
        except KeyError:
            line = "KeyError"
        finally:
            return line


###############################################################################
# Routing ######################################################################
###############################################################################

udb = UnQLite('test.udb')
pile = Pile(udb)
stamp_pattern = re.compile(r'^[a-zA-Z\d]{1,64}$')


@get('/pile')
def listing_handler():
    """Handles name listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(pile.list())


@post('/letter')
def creation_handler():
    """Handles letter creation"""
    try:
        # parse input data
        try:
            envelope = request.json
        except:
            raise ValueError
        # extract and validate contents
        try:
            stamp = envelope[0]
            letter = envelope[1]
            if stamp_pattern.match(stamp) is None:
                raise ValueError
        except (TypeError, KeyError):
            raise ValueError
        ret = pile.add(stamp, letter)
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(ret)


@get('/letter/<stamp>')
def listing_handler(stamp):
    """Handles letter listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(pile.find(stamp))


@put('/letter/update/<stamp>')
def update_handler(stamp):
    """Handles letter updates"""
    try:
        # parse input data
        try:
            envelope = request.json
        except:
            raise ValueError
        # extract and validate contents
        try:
            stamp = envelope[0]
            letter = envelope[1]
            if stamp_pattern.match(stamp) is None:
                raise ValueError
        except (TypeError, KeyError):
            raise ValueError
        # add new name and remove old name
        pile.bin(stamp)
        ret = pile.add(stamp, letter)
    except ValueError:
        response.status = 400
        return
    except KeyError as e:
        response.status = e.args[0]
        return
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(ret)


@delete('/letter/remove/<stamp>')
def delete_handler(stamp):
    """Handles letter removals"""
    try:
        # remove name
        pile.bin(stamp)
    except KeyError:
        response.status = 404
        return
    return


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


###############################################################################
# Application ##################################################################
###############################################################################

app = wsgi_app = application = bottle.default_app()


###############################################################################
# Utility ######################################################################
###############################################################################

def string_generator(max_length):
    length = randint(1, max_length)
    return ''.join([choice(ascii_letters + digits) for _ in range(length)])


class RandomEnvelope(list):
    def __init__(self, max_keys, max_lines, max_key_size, max_value_size):
        super().__init__()
        self.key_count = randint(1, max_keys)
        self.line_count = randint(1, max_lines)
        self.key_size = randint(1, max_key_size)
        self.value_size = randint(1, max_value_size)

    def key_generator(self):
        return [string_generator(self.key_size) for _ in range(self.key_count)]

    def line_generator(self, keys):
        return dict((key, string_generator(self.value_size)) for key in keys)

    def letter_generator(self):
        keys = self.key_generator()
        return [self.line_generator(keys) for _ in range(self.line_count)]

    def envelope_generator(self):
        stamp = string_generator(self.value_size)
        return [stamp, self.letter_generator()]


###############################################################################
# Api Testing ##################################################################
###############################################################################

app = TestApp(wsgi_app)


class TestLetterPosts(unittest.TestCase):
    def setUp(self):
        self.envelope = RandomEnvelope(100, 100, 10, 25).envelope_generator()

    @mock.patch('pll.pile.add')
    def test_post_200(self, mock_pile_add):
        mock_pile_add.return_value = json.dumps(self.envelope)
        response = app.post_json('/letter', self.envelope)
        assert response.json == json.dumps(self.envelope)

    @mock.patch('pll.pile.add')
    def test_post_409(self, mock_pile_add):
        mock_pile_add.side_effect = KeyError
        response = app.post_json('/letter', self.envelope, status=409)
        self.assertEqual(response.status_int, 409)


class TestLetterGets(unittest.TestCase):
    def setUp(self):
        self.envelope = RandomEnvelope(100, 100, 10, 25).envelope_generator()

    @mock.patch('pll.pile.find')
    def test_get_200(self, mock_pile_find):
        mock_pile_find.return_value = json.dumps(self.envelope)
        response = app.get('/letter/{}'.format(self.envelope[0]))
        assert response.json == json.dumps(self.envelope)


###############################################################################
# Model Testing ################################################################
###############################################################################

class TestPile(unittest.TestCase):
    def setUp(self):
        self.db = UnQLite(tempfile.mktemp())
        self.pile = Pile(self.db)
        self.db['1'] = "1"

    def test_list(self):
        assert self.pile.list() == [item for item in self.db]

    def test_find(self):
        assert self.pile.find('1') == self.db['1']


###############################################################################
# Main #########################################################################
###############################################################################

if __name__ == '__main__':
    bottle.run(host='127.0.0.1', port=8000)
