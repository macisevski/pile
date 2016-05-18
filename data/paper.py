from . import db


def get_paper(stamp):
    try:
        paper = db[stamp]
    except KeyError:
        paper = "KeyError"
    finally:
        return paper


@db.commit_on_success
def save_paper(stamp, paper):
    db[stamp] = paper
    return


@db.commit_on_success
def remove_paper(stamp):
    db.delete(stamp)
    return