import json

from bottle import post, get, put
from bottle import request, response

from data.letter import Letter


@post('/letter')
def creation_handler():
    """Handles letter creation"""
    try:
        # parse input data
        try:
            data = request.json
        except:
            raise ValueError
        stored = Letter(data).store_letter()
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
    return json.dumps(stored)


@get('/letter/<stamp>')
def listing_handler(stamp):
    """Handles letter listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'letter': pile.get_letter(stamp)})


@put('/pll/<stamp>')
def update_handler(stamp):
    """Handles name updates"""
    try:
        # parse input data
        try:
            letter = json.load(request.body)
        except:
            raise ValueError

        # extract and validate new name
        try:
            if namepattern.match(letter['name']) is None:
                raise ValueError
            newstamp = letter['name']
        except (TypeError, KeyError):
            raise ValueError

        # check if updated name exists
        if stamp not in pile.get_pile():
            raise KeyError(404)

        # check if new name exists
        if newstamp in pile.get_pile():
            raise KeyError(409)

    except ValueError:
        response.status = 400
        return
    except KeyError as e:
        response.status = e.args[0]
        return

    # add new name and remove old name
    letter.remove_letter(stamp)
    letter.add_letter(newstamp)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'name': newstamp})
