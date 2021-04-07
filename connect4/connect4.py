class Game:
    def __init__(self, rows: int=6, columns: int=7, player1: str="Red", player2: str="Yellow", data=None):
        """A connect 4 game, may or may not be largely copied from https://github.com/jayanam/connect4_python/blob/master/classes/board.py
        Hey at least I did change it a bit.
        
        Parameters:
            rows - An integer representing how many rows are in the board. Defaults to 6.
            columns - An integer representing how many columns are in the board. Defaults to 7.
            player1 - The name of player 1, defaults to Red
            player2 - The name of player 2, defaults to Yellow
            data - extra stuff about the players
        """
        self.rows = rows
        self.columns = columns
        self.players = [Player(0, name=player1), Player(1, name=player2)]
        self.move_count = 0
        self.data = data
        self.icon_mapping = {0: "🔴", 1: "🟡", 2: "🔵"}
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
        self.board = [[None for i in range(self.columns)] for j in range(self.rows)]
    
    # Check in all directions if a player has won (4 connected)
    def check_player_wins(self, player: "Player"=None) -> bool:
        playerid = player.getid() if player else not self.move_count&1

        # Check horizontal
        for c in range(self.columns-3):
            for r in range(self.rows):
                if self.board[r][c] == playerid and self.board[r][c+1] == playerid and self.board[r][c+2] == playerid and self.board [r][c+3] == playerid:
                    self.board[r][c] = 2
                    self.board[r][c+1] = 2
                    self.board[r][c+2] = 2
                    self.board[r][c+3] = 2
                    return True

        # Check vertical
        for c in range(self.columns):
            for r in range(self.rows-3):
                if self.board[r][c] == playerid and self.board[r+1][c] == playerid and self.board[r+2][c] == playerid and self.board [r+3][c] == playerid:
                    self.board[r][c] = 2
                    self.board[r+1][c] = 2
                    self.board[r+2][c] = 2
                    self.board[r+3][c] = 2
                    return True

        # Check positive diagonal
        for c in range(self.columns-3):
            for r in range(self.rows-3):
                if self.board[r][c] == playerid and self.board[r+1][c+1] == playerid and self.board[r+2][c+2] == playerid and self.board[r+3][c+3] == playerid:
                    self.board[r][c] = 3
                    self.board[r+1][c+1] = 2
                    self.board[r+2][c+2] = 2
                    self.board[r+3][c+3] = 2
                    return True

        # Check negative diagonal
        for c in range(self.columns-3):
            for r in range(3, self.rows):
                if self.board[r][c] == playerid and self.board[r-1][c+1] == playerid and self.board[r-2][c+2] == playerid and self.board[r-3][c+3] == playerid:
                    self.board[r][c] = 3
                    self.board[r-1][c+1] = 2
                    self.board[r-2][c+2] = 2
                    self.board[r-3][c+3] = 2
                    return True

        return False
    
    def generateMessage(self, icon_mapping: dict=None) -> str:
        if icon_mapping is None:
            icon_mapping = self.icon_mapping
        # https://stackoverflow.com/questions/33078554/mapping-dictionary-value-to-list
        return '\n'.join([' '.join([icon_mapping.get(self.board[r][c], "⚫") for c in range(self.columns)]) for r in range(self.rows)])
    
    def generateMessageInverse(self, icon_mapping: dict=None) -> str:
        """An alias for generateMessage to help with porting from the bitboard version"""
        return self.generateMessage(icon_mapping)
    # A player adds a new chip to a column of the board
    # The first free row is calculated, if the column is
    # full -1 is returns, otherwise the row to which the 
    # chip has been added
    def add_chip(self, column):
        for row in range(self.rows-1, -1, -1):
            cell_value = self.board[row][column]
            if cell_value is None:
                self.board[row][column] = self.move_count%2
                self.move_count += 1
                return row
        
        return -1
    

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
