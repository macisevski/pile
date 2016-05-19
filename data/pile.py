from . import db


def get_pile():
    return [item for item in db]


def find_letter(stamp):
    try:
        letter = db[stamp]
    except KeyError:
        letter = "KeyError"
    finally:
        return letter


@db.commit_on_success
def store_letter(stamp, letter):
    db[stamp] = letter
    return


@db.commit_on_success
def bin_letter(stamp):
    db.delete(stamp)
    return
