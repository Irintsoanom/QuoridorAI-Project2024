from enum import Enum

class PlayerType(Enum):
    ENEMY = 'ENEMY'
    CURRENT = 'CURRENT'

class Game:
    def __init__(self):       
        self.lives = 3
        self.errors = None
        self.board = []
        self.current = 0
        self.enemy = 1
        self.blockers = [10, 10]

    def setState(self, message):
        state = message['state']
        self.lives = message['lives']
        self.errors = message['errors']
        self.current = state['current']
        self.board = state['board']
        self.blockers = state['blockers']
        self.enemy = 1 if self.current == 0 else 0
    
    def getPlayerPosition(self, playerType: PlayerType):
        player = self.current if playerType == PlayerType.CURRENT else self.enemy
        for i, list in enumerate(self.board):
            for j, item in enumerate(list):
                if item == player:
                    return (i, j)
        return (None, None)
    
    
    def play(self):
        print(self.getPlayerPosition(PlayerType.CURRENT))
        print(self.getPlayerPosition(PlayerType.ENEMY))
        nextPotentialPositions = self.getNextPotentialPositions()
        pass

    def getNextPotentialPositions(self):
        player = self.getPlayerPosition(PlayerType.CURRENT)
        xPos, yPos = player[0], player[1]

        while 0 <= xPos < 10:
            #Forward
            if xPos + 1 == 3  and self.current == 0:
                nextPosition = (xPos + 2, yPos)
            elif (xPos - 1 == 3 and self.current == 1):
                nextPosition = (xPos - 2, yPos)

            #Moving back
            if xPos + 1 == 3 and self.current == 0:
                nextPosition = (xPos - 2, yPos)
            elif xPos - 1 == 3 and self.current == 1:
                nextPosition = (xPos + 2, yPos)

        
        #Moving left and right
        while 0 <= yPos < 17:
            if yPos - 1 == 3:
                nextPosition = (xPos, yPos - 2)
            else:
                nextPosition = (xPos, yPos + 2)

        return nextPosition
        
    def getAvailableMove(self):
        pass

    def isPieceOccupied(self):
        pass

    def isWallOccupied(self):
        pass

    def __str__(self):
      return f"My state is {self.lives}"