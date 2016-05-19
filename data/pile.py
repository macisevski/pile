
class Pile:
    def __init__(self, db):
        self.db = db

    def get_pile(self):
        return [item for item in self.db]

    def find_letter(self, stamp):
        try:
            letter = self.db[stamp]
        except KeyError:
            raise KeyError
        finally:
            return letter

    def store_letter(self, stamp, letter):
        self.db[stamp] = letter
        return letter

    def bin_letter(self, stamp):
        self.db.delete(stamp)
        return
