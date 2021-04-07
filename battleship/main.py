"""Battleship library, written in python.
Heavily inspired by the python chess engine: https://github.com/niklasf/python-chess
Svg part is mostly copied from svg submodule of python chess engine.
"""
from dataclasses import dataclass, field
from typing import List, Union, Optional
from io import StringIO
import string
import typing

# Variables for tiles

TileType = int
# An integer
TILE_TYPES = [WATER, CARRIER, BATTLESHIP, DESTROYER, SUBMARINE, PATROL] = range(1, 7)
# The types of tiles
TILE_SYMBOLS = ["w", "h"]
# The tile symbols
TILE_NAMES = ["water", "carrier", "battleship", "destroyer", "submarine", "patrol boat"]
# The names of all the tiles
TILE_SIZES = {
    "w": None,
    "c": 5,
    "b": 4,
    "d": 3,
    "s": 3,
    "p": 2
}
# How much space each tile ranges across (water is none since it's a singular tile)
PLAYERS = [True, False]
# Variables for svg stuff

SVG_SIZE = 45
# The size of the svgs
SHIP_SVG = """<g id="ship"> <rect style="fill:#404040;stroke-width:0.264583" id="rect10" width="100%" height="100%" x="0" y="0"/> </g>"""
# Temporary svg for ships until each has their own
SVG_TILES = {
    "w": """<g id="water"> <rect style="fill:#6EB0F8;fill-rule:evenodd;stroke-width:0.264583" id="rect12" width="100%" height="100%" x="0" y="0" /> </g>""",
    "c": SHIP_SVG,
    "b": SHIP_SVG,
    "d": SHIP_SVG,
    "s": SHIP_SVG,
    "p": SHIP_SVG,
    "w_hit": """"""
}
# The actual svgs

def ship_symbol(piece_type: TileType) -> str:
    return typing.cast(str, TILE_SYMBOLS[piece_type])

def piece_name(piece_type: TileType) -> str:
    return typing.cast(str, TILE_NAMES[piece_type])

def blank_board():
    return [[Tile.from_symbol("w") for x in range(10)] for x in range(10)]

EMOJI_SHIP_SYMBOLS = {
    "c": "<:carrier:770891368112979968>",
    "b": "<:battleship:770891580936159262>",
    "d": "<:destroyer:770891728118349844>",
    "s": "<:submarine:770891870464114688>",
    "p": "<:patrolboat:770892013179502592>"
}

@dataclass()
class Tile:
    tile_type: TileType
    """The type of tile, either ``0 (water)``, ``1 (carrier)``, ``2 (battleship)``, ``3 (destroyer)``, ``4 (submarine)``, or ``5 (patrol boat)``"""

    player: bool = None
    """Whether it's player 1 or 2, 1 is True and 2 is False. None is for water."""

    isHit: bool = False
    """Whether a tile has been hit or not."""
    
    @property
    def name(self) -> str:
        return TILE_NAMES[self.tile_type]

    @property
    def symbol(self) -> str:
        """
        Gets the symbol ``H``, ``W`` for P1
        tiles or the lower-case variants for P2.
        """
        symbol = ship_symbol(self.tile_type)
        return symbol.upper() if self.player else symbol
    
    def emoji(self) -> str:
        """
        Gets the discord emoji for the piece.
        """
        return EMOJI_SHIP_SYMBOLS[self.symbol]
    
    def size(self):
        return TILE_SIZES[self.symbol]
    
    def hit(self):
        """
        Sets the tile as hit. Returns the tile to allow for chaining of expressions.
        """
        self.isHit = True
        return self

    def __hash__(self) -> int:
        return hash(self.tile_type * self.player)
    
    def __repr__(self) -> str:
        return f"Tile.from_symbol({self.symbol!r})"
    
    def __str__(self) -> str:
        p = self.player
        if self.player == None:
            p = ""
        elif self.player:
            p = ", 'Player 1'"
        elif not self.player:
            p = ", 'Player 2'"
        return f"battleship.Tile({self.name!r}{p})"
    
    @classmethod
    def from_symbol(cls, symbol: str) -> 'Tile':
        """
        Creates a :class:`~battleship.Tile` instance from a piece symbol.
        :raises: :exc:`ValueError` if the symbol is invalid.
        """
        if symbol.lower() == "w":
            return cls(TILE_SYMBOLS.index(symbol.lower()), None)
        return cls(TILE_SYMBOLS.index(symbol.lower()), symbol.isupper())


@dataclass()
class Board:
    board: List[List[Tile]] =  field(default_factory=blank_board)
    
    def print(self):
        print(self)
    
    def __iter__(self):
        self.n = 1
        return self

    def __next__(self):
        if self.n <= len(self.board):
            retval = self.board[self.n - 1]
            self.n += 1
            return retval
        else:
            raise StopIteration


@dataclass()
class Game:
    """The actual battleship game.
    
    Required Parameters:
        None
    Optional Parameters:
        board: List[Tile]
    """
    #def __init__(self, p1: discord.Member, p2: discord.Member, p1_channel: discord.TextChannel, p2_channel: discord.TextChannel, game_number: int = 0, extra_data: dict={}):
    
    def move(self, move: str):
        if len(move) != 2:
            return {"result": "error", "debug": "invalidLen", "message": "Invalid move. The move given was either too long or too short."}
        letter, number = move.upper()
        if(letter not in string.ascii_uppercase) and (number):
            return {"result": "error", "debug": "invalidMove", "message": "Invalid move. Letters range from A-J, and numbers from 0-10."}

        letter = string.ascii_uppercase.find(letter)
        location = self.board[letter][number]

        if location.isHit:
            return {"result": "error", "debug": "alreadyHit", "message": "This location has already been hit. Please try again."}
        elif location.symbol == "w":
            self.board[letter][number].hit()
            return {"result": "miss", "ship": "water", "message": "You missed."}
        else:
            self.board[letter][number].hit()
            return {"result": "hit", "ship": f"{self.board[letter][number].name}", "message": f"You hit a ship."}
    
    #def mark(self,)

if __name__ == "__main__":
    from PIL import Image
    import io
    # import img

    # Tile.from_symbol("w").svg().write(open("test.svg", "wb"))
    # Testing stuff
    for x,y in enumerate(Board()):
        print(x)
