from bottle import request, response
from bottle import post, get, put, delete
# import re
import json
from data.pile import get_pile, store_letter

# stamppattern = re.compile(r'^[a-zA-Z\d]{1,64}$')


@post('/letter')
def creation_handler():
    """Handles letter creation"""
    try:
        # parse input data
        try:
            data = request.json
            print(data)
        except:
            raise ValueError

        if data is None:
            raise ValueError
        # extract and validate name
        try:
            # if namepattern.match(letter['stamp']) is None:
            #    raise ValueError
            stamp = data[0]
            letter = data[1]
            print(stamp)
        except (TypeError, KeyError):
            raise ValueError
        # check for existence
        pile = get_pile()
        print(pile)
        print(stamp in pile)
        if stamp in pile:
            raise KeyError
    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return
    # add name
    print(letter)
    store_letter(stamp, letter)
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(letter)


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
