"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

##### IMPORTS #####
import json
import os
import sys
import io
import base64
import hashlib
import requests
from typing import List
from PIL import Image, ImageFont, ImageDraw

sys.setrecursionlimit(4000)
UPLOAD_URL = os.environ["UPLOAD_URL"]

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

    
    def generate_image(self, winning_tiles=None) -> str:
        """Returns a string with a url for the board.
        
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
            # Remove the alpha channel so that the image can be saved as JPG, which is much smaller than PNG
            img = img.convert('RGB')
            # Save the image as JPG to the output BytesIO
            img.save(output, format="JPEG")
            # Move the pointer to the beginning of the BytesIO
            output.seek(0)
            
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cached_boards.json"), "r") as f:
                decodeval = base64.b64encode(output.getvalue()).decode('ascii')
                url = json.load(f).get(decodeval, None)

            if url is None:
                try:
                    response = requests.post(
                        UPLOAD_URL + "/upload-image",
                        files={"image": output},
                        data={"password": hashlib.sha3_512(os.getenv("IMAGE_API_PASSWORD").encode()).hexdigest()}
                    )
                except requests.exceptions.ConnectionError:
                    # If we made too many requests, we say that it failed
                    r.status_code = "Connection Refused"
                response.raise_for_status()
                url = UPLOAD_URL + response.text

                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cached_boards.json"), "w") as f:
                    json.dump({decodeval: url}, f)
            
            return url if response.ok else False
    
    def move_valid(self, index) -> bool:
        """Returns a bool stating whether a move is valid or not"""
        return not self.board[index-1]
    
    async def best_move(self, player: int, other_player) -> int:
        # https://www.freecodecamp.org/news/how-to-make-your-tic-tac-toe-game-unbeatable-by-using-the-minimax-algorithm-9d690bad4b37/
        return (await self.minimax(player, other_player))-1
    
    async def minimax(self, player, other_player):
        # available spots
        availSpots = [x+1 for x in range(9) if self.board[x] == 0]

        # checks for the terminal states such as win, lose, and tie 
        # and returning a value accordingly
        if self.winning(other_player):
            return {"score": -10}
        elif self.winning(player):
            return {"score": 10}
        elif len(availSpots) == 0:
            return {"score": 0}
        
        the_moves = []
        for j in availSpots:
            self.make_move_index(j)
            # collect the score resulted from calling minimax 
            # on the opponent of the current player

            the_moves.append({
                "index": j,
                "score": (await self.minimax(player, other_player))["score"]
            })

            self.undo_move_index(j)
        
        scoreLambda = lambda x: x["score"]
        if (not self.move_count%2 == player):
            the_best_move = max(the_moves, key=scoreLambda)
        else:
            the_best_move = min(the_moves, key=scoreLambda)
        
        return the_best_move
