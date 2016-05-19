from unqlite import UnQLite
from .pile import Pile

db = UnQLite('test.udb')
pile = Pile(db)
