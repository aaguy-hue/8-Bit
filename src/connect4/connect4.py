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

class Game:
    """A connect 4 game, original idea came from https://github.com/jayanam/connect4_python/blob/master/classes/board.py.
    
    However, this has been modified to do things like use bitboards for further optimizations, and it also does slightly different things.

    Parameters:
        rows - An integer representing how many rows are in the board. Defaults to 6.
        columns - An integer representing how many columns are in the board. Defaults to 7.
        player1 - The name of player 1, defaults to Red
        player2 - The name of player 2, defaults to Yellow
        data - extra stuff about the players
    """

    def __init__(self, rows: int=6, columns: int=7, player1: str="Red", player2: str="Yellow", data=None):
        self.rows = rows
        self.columns = columns
        self.players = [Player(0, name=player1), Player(1, name=player2)]
        self.move_count = 0
        self.data = data
        self.icon_mapping = {0: "🔴", 1: "🟡"}
        self.data = data
        # Make a clear board
        # None = empty space
        # 0 = space has a player 1 (id 0) piece
        # 1 = space has a player 2 (id 1) piece
        # 2 = winning tiles
        self.clear()

    def __hash__(self):
        return hash((self.players[0], self.players[1]))
    
    def __eq__(self, other):
        # One game per group of people
        return isinstance(other, self.__class__) and self.players[0] == other.players[0] and self.players[1] == other.players[1]

    def __ne__(self, other):
        return not (isinstance(other, self.__class__) and self.players[0] == other.players[0] and self.players[1] == other.players[1])

    # Clear the board
    def clear(self):
        self.mask = 0
        self.position = 0
    
    # Check in all directions if a player has won (4 connected)
    def gameResults(self, player: "Player"=None) -> int:
        """Gets who won.
        Return True if the current player won, or return 0 if it's a tie, and -1 if no one won
        """
        # Horizontal check
        m = self.position & (self.position >> 7)
        if m & (m >> 14):
            return True    # True = 1
        
        # Diagonal \
        m = self.position & (self.position >> 6)
        if m & (m >> 12):
            return True    # True = 1
        # Diagonal /
        m = self.position & (self.position >> 8)
        if m & (m >> 16):
            return True    # True = 1
        # Vertical
        m = self.position & (self.position >> 1)
        if m & (m >> 2):
            return True    # True = 1
        
        # If the board is full (tie)
        # 279258638311359 is the value if the board is filled and the sentinal row is empty
        if self.mask >= 279258638311359:
            return False    # False = 0
        
        # Nothing found
        return -1
    
    def winning_tiles(self):
        """Checks for winning the old and slow way in order to get the winning tiles.
        
        Only use this for displaying, as it's a bit slower.
        
        Returns the winning tiles or False if there was a tie, or otherwise None."""
        playerid = self.move_count % 2
        board = self.to_array()
        
        # Check horizontal
        for c in range(self.columns-3):
            for r in range(self.rows):
                if board[r][c] == playerid and board[r][c+1] == playerid and board[r][c+2] == playerid and board [r][c+3] == playerid:
                    return [[r, c], [r, c+1], [r, c+2], [r, c+3]]
        
        # Check vertical
        for c in range(self.columns):
            for r in range(self.rows-3):
                if board[r][c] == playerid and board[r+1][c] == playerid and board[r+2][c] == playerid and board [r+3][c] == playerid:
                    return [[r, c], [r+1, c], [r+2, c], [r+3, c]]
        
        # Check positive diagonal
        for c in range(self.columns-3):
            for r in range(self.rows-3):
                if board[r][c] == playerid and board[r+1][c+1] == playerid and board[r+2][c+2] == playerid and board[r+3][c+3] == playerid:
                    return [[r, c], [r+1, c+1], [r+2, c+2], [r+3, c+3]]

        # Check negative diagonal
        for c in range(self.columns-3):
            for r in range(3, self.rows):
                if board[r][c] == playerid and board[r-1][c+1] == playerid and board[r-2][c+2] == playerid and board[r-3][c+3] == playerid:
                    return [[r, c], [r-1, c+1], [r-2, c+2], [r-3, c+3]]
        
        # Tie
        if self.mask >= 279258638311359:
            return False
        
        # Nothing
        return None
    
    def generateMessage(self, winning_tiles=None, icon_mapping: dict=None) -> str:
        if icon_mapping is None:
            icon_mapping = self.icon_mapping
        if winning_tiles is None:
            winning_tiles = []
        
        board = self.to_array()
        # https://stackoverflow.com/questions/33078554/mapping-dictionary-value-to-list
        return '\n'.join([' '.join(["🔵" if [r,c] in winning_tiles else icon_mapping.get(board[r][c] if board[r][c] is None else not board[r][c], "⚫") for c in range(self.columns)]) for r in range(self.rows)])
    
    # A player adds a new chip to a column of the board
    # If the column is full -1 is returned
    def add_chip(self, col):
        # The position is now the board of the other player
        new_mask = self.mask | (self.mask + (1 << (col*7)))
        if new_mask == self.mask:
            return -1
        
        self.mask = new_mask
        self.position = self.position ^ self.mask
        self.move_count += 1
        
    def to_array(self):
        arrangement = [[5, 12, 19, 26, 33, 40, 47], [4, 11, 18, 25, 32, 39, 46], [3, 10, 17, 24, 31, 38, 45], [2, 9, 16, 23, 30, 37, 44], [1, 8, 15, 22, 29, 36, 43], [0, 7, 14, 21, 28, 35, 42]]
        theMaskBytes = bin(self.mask)[2:].rjust(49, '0')
        thePositionBytes = bin(self.position)[2:].rjust(49, '0')
        thePlayer = self.move_count%2
        # no idea why, but making the index for the bytes negative (and subtracting one since negative indexing starts from 1 rather than 0) works somehow
        return [[None if not int(theMaskBytes[-(arrangement[r][c])-1]) else thePlayer if int(thePositionBytes[-(arrangement[r][c])-1]) else (not thePlayer) for c in range(self.columns)] for r in range(len(arrangement))]

class Player:
    def __init__(self, id, name=None):
        self.id = id
        self.name = name
        
    def getid(self):
        return self.id

    def get_color(self):
        if self.id == 0:
            return (255,0,0)
        else:
            return (255,255,0)

    def get_name(self):
        if self.id == 0:
            return "Red"
        else:
            return "Yellow"

def predict_winner(game: Game, isMaximizing: bool):
    pass

def get_optimal_move(game: Game, isMaximizing: bool):
    """Figures out the optimal next move (could be used for something like AI)
    
    Takes in 2 arguments:
        game - An instance of the connect4.Game class
        isMaximizing - A bool indicating whether the player is red or yellow (player 1 or 2). Important for implementation reasons.

    Based on https://www.youtube.com/watch?v=trKjYdBASyQ.
    Player 1 is the maximizing player, Player 2 is the minimizing player
    """
    return 1