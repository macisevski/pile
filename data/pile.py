
class Pile:
    def __init__(self, db):
        self.db = db

    def get_pile(self):
        return [item for item in self.db]

    def find(self, stamp):
        try:
            letter = self.db[stamp]
        except KeyError:
            raise KeyError
        finally:
            return letter

    def add(self, envelope):
        if self.find():
            raise KeyError
        return pile.store_letter(self.stamp, self.letter)

    def store_letter(self, stamp, letter):
        self.db[stamp] = letter
        return letter

    def bin_letter(self, stamp):
        self.db.delete(stamp)
        return
