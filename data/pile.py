
class Pile:
    def __init__(self, db):
        self.db = db

    def get_pile(self):
        return [item for item in self.db]

    def find(self, stamp):
        try:
            return self.db[stamp]
        except KeyError:
            raise KeyError

    def add(self, stamp, letter):
        print(123)
        print(self.find(stamp))
        if self.find(stamp):
            raise KeyError
        self.db[stamp] = letter
        return self.find(stamp)

    def bin(self, stamp):
        self.db.delete(stamp)
        return
