from bottle import post, get, put
from bottle import request, response
import json
import re
from data import pile

stamp_pattern = re.compile(r'^[a-zA-Z\d]{1,64}$')


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


@put('/pll/<stamp>')
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
        # check if updated stamp exists
        if stamp not in pile.get_pile():
            raise KeyError(404)
    except ValueError:
        response.status = 400
        return
    except KeyError as e:
        response.status = e.args[0]
        return
    # add new name and remove old name
    pile.bin(stamp)
    ret = pile.add(stamp, letter)
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(ret)
