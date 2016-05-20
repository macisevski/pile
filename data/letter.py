

class Letter:
    def get_line(letter, signet):
        try:
            line = letter[signet]
        except KeyError:
            line = "KeyError"
        finally:
            return line

