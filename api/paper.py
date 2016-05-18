from bottle import request, response
from bottle import get, put, delete
import re
import json
from data import pile, paper

namepattern = re.compile(r'^[a-zA-Z\d]{1,64}$')


@get('/paper/<stamp>')
def listing_handler(stamp):
    """Handles name listing"""
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'paper': paper.get_paper(stamp)})


@put('/pile/<stamp>')
def update_handler(stamp):
    """Handles name updates"""
    try:
        # parse input data
        try:
            paper = json.load(request.body)
        except:
            raise ValueError

        # extract and validate new name
        try:
            if namepattern.match(paper['name']) is None:
                raise ValueError
            newstamp = paper['name']
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
    paper.remove_paper(stamp)
    paper.add_paper(newstamp)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'name': newstamp})
