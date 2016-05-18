from . import db


def get_record(stamp, signet):
    try:
        record = db[stamp][signet]
    except KeyError:
        record = "KeyError"
    finally:
        return record