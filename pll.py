import json
import re

import bottle
from bottle import post, get, put, delete
from bottle import request, response
from unqlite import UnQLite


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
    return json.dumps({'letter': pile.get_letter(stamp)})


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
# Main #########################################################################
###############################################################################

app = wsgi_app = application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host='127.0.0.1', port=8000)
