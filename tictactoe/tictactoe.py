##### IMPORTS #####
import os
import sys
import io
import json
from typing import List
from PIL import Image, ImageFont, ImageDraw

sys.setrecursionlimit(4000)

class Game:
    # Scoring for AI
    SCORE_WIN = 1
    SCORE_TIE = 0
    SCORE_LOSE = -1
    
    TILE_BASE_COORDS = (10, 10)
    STAR_BASE_COORDS = (5, 5)
    
    def __init__(self, p1: str="Player 1", p2: str="Player 2", data: dict=None):
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.players = [p1, p2]
        self.move_count = 0
        self.data = data
    
    def __str__(self):
        return str(self.board)
    
    def __repr__(self):
        return repr(self.board)
    
    def __hash__(self):
        return hash((self.players[0], self.players[1]))
    
    def __eq__(self, other):
        # One game per group of people
        return isinstance(other, self.__class__) and self.players[0] == other.players[0] and self.players[1] == other.players[1]

    def __ne__(self, other):
        return not (isinstance(other, self.__class__) and self.players[0] == other.players[0] and self.players[1] == other.players[1])
    
    def make_move_rc(self, row, col, player=None) -> bool:
        """Makes a move in the tic tac toe game by specifying a row and column.
        
        Takes in the row and column of the place to put the token.
        Returns a boolean stating whether the move was valid.
        
          1,1  |  1,2  |  1,3  
        -----------------------
          2,1  |  2,2  |  2,3  
        -----------------------
          3,1  |  3,2  |  3,3  """
        
        theIndex = (row-1)*3+col
        if self.board[theIndex]:
            return False
        
        self.board[theIndex] = player if player else self.move_count % 2 + 1
        self.move_count += 1

        return True
    
    def make_move_index(self, index, player=None) -> bool:
        """Makes a move in the tic tac toe game by specifying an index.
        
        Takes in a parameter, index, which represents the index of a spot.
        Returns a boolean stating whether the move was valid.
        
           1   |   2   |   3   
        -----------------------
           4   |   5   |   6   
        -----------------------
           7   |   8   |   9   """
        
        if self.board[index-1]:
            return False
        
        self.board[index-1] = player if player else self.move_count % 2 + 1
        self.move_count += 1
        return True
    
    def undo_move_index(self, index) -> bool:
        """Undoes a move in the tic tac toe game by specifying an index.
        
        Takes in a parameter, index, which represents the index of a spot.
        Returns a boolean stating whether the undo operation was valid.
        
           1   |   2   |   3   
        -----------------------
           4   |   5   |   6   
        -----------------------
           7   |   8   |   9   """
        
        if not self.board[index-1]:
            return False
        
        self.board[index-1] = 0
        self.move_count -= 1
        return True
        
    def game_results(self):
        """Returns the winning tiles, which is None if the game isn't won. Returns False if the game is a tie."""
        player = not self.move_count % 2
        playerlst = [player+1]*3
        # Horizontal (-)
        if playerlst == [self.board[0], self.board[1], self.board[2]]:
            return 0,1,2
        elif playerlst == [self.board[3], self.board[4], self.board[5]]:
            return 3,4,5
        elif playerlst == [self.board[6], self.board[7], self.board[8]]:
            return 6,7,8
        
        # Vertical (|)
        if playerlst == [self.board[0], self.board[3], self.board[6]]:
            return 0,3,6
        elif playerlst == [self.board[1], self.board[4], self.board[7]]:
            return 1,4,7
        elif playerlst == [self.board[2], self.board[5], self.board[8]]:
            return 2,5,8
        
        # Diagonal (\)
        if playerlst == [self.board[0], self.board[4], self.board[8]]:
            return 0,4,8

        # Diagonal (/)
        if playerlst == [self.board[2], self.board[4], self.board[6]]:
            return 2,4,6
        
        # If no one wins, and the board is full
        if all(self.board):
            return False
        
        return None
    
    def winning(self, player):
        if (
        (self.board[0] == player and self.board[1] == player and self.board[2] == player) or
        (self.board[3] == player and self.board[4] == player and self.board[5] == player) or
        (self.board[6] == player and self.board[7] == player and self.board[8] == player) or
        (self.board[0] == player and self.board[3] == player and self.board[6] == player) or
        (self.board[1] == player and self.board[4] == player and self.board[7] == player) or
        (self.board[2] == player and self.board[5] == player and self.board[8] == player) or
        (self.board[0] == player and self.board[4] == player and self.board[8] == player) or
        (self.board[2] == player and self.board[4] == player and self.board[6] == player)
        ):
            return True
        else:
            return False

    
    def generate_image(self, winning_tiles=None) -> bytes:
        """Returns bytes in a png format for the board.
        
        Optionally takes in the winning tiles, passed in from game_results()."""
        # Thank god for this: https://stackoverflow.com/a/45041002
        curr_file = os.path.abspath(__file__)
        curr_dir = os.path.dirname(curr_file)

        img = Image.open(os.path.join(curr_dir, "images/grid.png"))
        x = Image.open(os.path.join(curr_dir, "images/X.png"))
        o = Image.open(os.path.join(curr_dir, "images/O.png"))
        if winning_tiles:
            star = Image.open(os.path.join(curr_dir, "images/WinningTile.png"))
        else:
            winning_tiles = [None]
        drawing = ImageDraw.Draw(img)
        font = ImageFont.truetype(os.path.join(curr_dir, "fonts/times_new_roman_bold.ttf"), 100)

        [[img.paste(x, (Game.TILE_BASE_COORDS[0]+100*(i%3), Game.TILE_BASE_COORDS[1]+100*(i//3))) if token == 1 else img.paste(o, (Game.TILE_BASE_COORDS[0]+100*(i%3), Game.TILE_BASE_COORDS[1]+100*(i//3))) if token == 2 else drawing.text(((i%3)*100 +25, (i//3)*100 -10), str(i+1), (128,128,128), font=font), img.paste(star, (Game.STAR_BASE_COORDS[0]+100*(i%3), Game.STAR_BASE_COORDS[1]+100*(i//3))) if i in winning_tiles else None] for i, token in enumerate(self.board)]
        
        with io.BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            val = output.getvalue()
            return val
    
    def move_valid(self, index) -> bool:
        """Returns a bool stating whether a move is valid or not"""
        return not self.board[index-1]
    
    @property
    def emptyIndexies(self) -> List[int]:
        """Returns a list of indexes for the available spots"""
        return [x+1 for x in range(9) if self.board[x] == 0]
    
    async def best_move(self, player: int, other_player) -> int:
        # https://www.freecodecamp.org/news/how-to-make-your-tic-tac-toe-game-unbeatable-by-using-the-minimax-algorithm-9d690bad4b37/
        return (await self.minimax(player, other_player))-1
    
    async def minimax(self, player, other_player):
        # available spots
        availSpots = self.emptyIndexies

        # checks for the terminal states such as win, lose, and tie 
        # and returning a value accordingly
        if self.winning(other_player):
            return -10
        elif self.winning(player):
            return 10
        elif len(availSpots) == 0:
            return 0
        
        the_moves = []
        for j in availSpots:
            self.make_move_index(j)
            # collect the score resulted from calling minimax 
            # on the opponent of the current player

            the_moves.append({
                "index": j,
                "score": await self.minimax(player, other_player)
            })

            self.undo_move_index(j)
        
        scoreLambda = lambda x: x["score"]
        if (not self.move_count%2 == player):
            the_best_move = max(the_moves, key=scoreLambda)["index"]
        else:
            the_best_move = min(the_moves, key=scoreLambda)["index"]
        
        return the_best_move
