
class Pile:
    def __init__(self, db):
        self.db = db

    def list(self):
        return [item for item in self.db]

    def find(self, stamp):
        try:
            return self.db[stamp]
        except KeyError:
            raise

    def add(self, stamp, letter):
        if not self.db.exists(stamp):
            self.db[stamp] = letter
        else:
            raise KeyError
        return self.find(stamp)

    def bin(self, stamp):
        try:
            self.db.delete(stamp)
        except KeyError:
            raise
