"""A class used to manage having multiple games at once."""

class GameAlreadyExistsError(Exception): pass

# https://stackoverflow.com/a/41281734
class GameManager(set):
    def add(self, value):
        # https://stackoverflow.com/a/17735466
        if value in self or [True for other in self if not set(value.data.values()).isdisjoint(other.data.values())]:
            raise GameAlreadyExistsError('Game {!r} already exists'.format(value))
            return
        super().add(value)

    def update(self, values):
        for value in values:
            # https://stackoverflow.com/a/17735466
            if value in self or [True for other in self if not set(value.data.values()).isdisjoint(other.data.values())]:
                raise GameAlreadyExistsError('Game {!r} already exists'.format(error_values))
                return
        super().update(values)
    
    def endGame(self, game):
        self.remove(game)
    
    def gameExists(self, game) -> bool:
        return game in self
    
    def getGame(self, player1):
        for game in self:
            if player1 in game.data.values():
                return game

def setup(bot):
    pass
