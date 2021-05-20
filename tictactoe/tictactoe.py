##### IMPORTS #####
import io
import os
from PIL import Image, ImageFont, ImageDraw

class Game:
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
    
    def make_move_rc(self, row, col) -> bool:
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
        
        self.board[theIndex] = self.move_count % 2 + 1
        self.move_count += 1

        return True
    
    def make_move_index(self, index) -> bool:
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
        
        self.board[index-1] = self.move_count % 2 + 1
        self.move_count += 1
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
            return output.getvalue()
    