SENTINAL_ROW = [6, 13, 20, 27, 34, 41, 48]

class Game:
    def __init__(self, rows: int=6, columns: int=7, player1: str="Red", player2: str="Yellow", data=None):
        """A connect 4 game, may or may not be largely copied from https://github.com/jayanam/connect4_python/blob/master/classes/board.py
        Hey at least I did change it a bit.
        
        Parameters:
            rows - An integer representing how many rows are in the board. Defaults to 6.
            columns - An integer representing how many columns are in the board. Defaults to 7.
            player1 - The name of player 1, defaults to Red
            player2 - The name of player 2, defaults to Yellow
        """
        self.rows = rows
        self.columns = columns
        self.players = [Player(0, name=player1), Player(1, name=player2)]
        self.data = data
        self.icon_mapping = {0: "🔴", 1: "🟡", 2: "🔵"}
        self.move_count = 0
        # Make a clear board
        # None = empty space
        # 0 = space has a player 1 (id 0) piece
        # 1 = space has a player 2 (id 1) piece
        # 2 = winning tiles
        self.clear()

    # Clear the board
    def clear(self):
        # Mask, Player 1 bitboard (get Player 2 by doing XOR operation)
        self.mask = int('0000000000000000000000000000000000000000000000000', 2)
        self.position = int('0000000000000000000000000000000000000000000000000', 2)    

    # Check in all directions if a player has won (4 connected)
    # How to understand? https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md#are-there-four-in-a-row
    def check_player_wins(self):
        # Horizontal check
        m = self.position & (self.position >> 7)
        if m & (m >> 14):
            return True
        # Diagonal \
        m = self.position & (self.position >> 6)
        if m & (m >> 12):
            return True
        # Diagonal /
        m = self.position & (self.position >> 8)
        if m & (m >> 16):
            return True
        # Vertical
        m = self.position & (self.position >> 1)
        if m & (m >> 2):
            return True
        # Nothing found
        return False
    
    # def generateMessage(self, icon_mapping: dict=None) -> str:
    #     if icon_mapping is None:
    #         icon_mapping = self.icon_mapping
    #     # https://stackoverflow.com/a/16660062
    #     mask_bits = [(self.mask >> bit) & 1 for bit in range(48, -1, -1)]
    #     position_bits = [(self.position >> bit) & 1 for bit in range(48, -1, -1)]
    #     final = ""
    #     for i, (m, p) in enumerate(zip(mask_bits, position_bits)):
    #         if not i % 8:
    #             final += "\n"
    #         elif m & p:
    #             final += self.icon_mapping[self.move_count&1] + " "
    #         elif m:
    #             final += self.icon_mapping[1 - self.move_count&1] + " "
    #         else:
    #             final += "⚫ "
    #     # final = '\n'.join(final[i:i+6] for i in range(0, len(final), 6))
    #     return final
    
    def generateMessageInverse(self, icon_mapping: dict=None) -> str:
        """generateMessage() but the player tokens are switched.
        Why would you do this? Let's say I have the player move, then generate the new message.
        Since the turn has switched, this will now generate the message with the wrong icons.
        As such this function exists."""
        if icon_mapping is None:
            icon_mapping = self.icon_mapping
        # https://stackoverflow.com/a/16660062
        # mask_bits = [(self.mask >> bit) & 1 for bit in range(48, -1, -1)]
        # position_bits = [((self.mask ^ self.position) >> bit) & 1 for bit in range(48, -1, -1)]
        mask_bits = [int(x) for x in bin(self.mask)[2:].ljust(49, "0")]
        position_bits = [int(x) for x in bin(self.position)[2:].ljust(49, "0")]
        final = [5, 12, 19, 26, 33, 40, 47, '\n', 4, 11, 18, 25, 32, 39, 46, '\n', 3, 10, 17, 24, 31, 38, 45, '\n', 2, 9, 16, 23, 30, 37, 44, '\n', 1, 8, 15, 22, 29, 36, 43, '\n', 0, 7, 14, 21, 28, 35, 42]
        for i, (m, p) in enumerate(zip(mask_bits, position_bits)):

            if i in SENTINAL_ROW:
                continue

            tomodify = final.index(i)
            if m & p:
                final[tomodify] = self.icon_mapping[self.move_count&1] + " "
            elif m:
                final[tomodify] = self.icon_mapping[1 - self.move_count&1] + " "
            else:
                final[tomodify] = "⚫ "
        
        # final = '\n'.join(final[i:i+6] for i in range(0, len(final), 6))
        return ''.join(final)
    
    # A player adds a new chip to a column of the board
    # The first free row is calculated, if the column is
    # full -1 is returns, otherwise the row to which the 
    # chip has been added
    def add_chip(self, col):
        # The position is now the board of the other player
        new_mask = self.mask | (self.mask + (1 << (col*7)))
        if new_mask == self.mask:
            return -1
        
        self.mask = new_mask
        self.position = self.position ^ self.mask
        self.move_count += 1

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
