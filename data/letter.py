import re
from . import pile


class Letter:
    stamppattern = re.compile(r'^[a-zA-Z\d]{1,64}$')

    def __init__(self, envelope):
        # extract and validate contents
        try:
            if self.stamppattern.match(envelope[0]) is None:
                raise ValueError
            self.stamp = envelope[0]
            self.letter = envelope[1]
        except (TypeError, KeyError):
            raise ValueError

    def isduplicate(self):
        return self.stamp in pile.get_pile()

    def store_letter(self):
        if self.isduplicate():
            raise KeyError
        return pile.store_letter(self.stamp, self.letter)

    def get_line(letter, signet):
        try:
            line = letter[signet]
        except KeyError:
            line = "KeyError"
        finally:
            return line
