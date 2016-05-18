from . import db


def get_pile():
    return [item for item in db]
