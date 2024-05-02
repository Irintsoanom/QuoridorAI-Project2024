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
        self.playerPosition = ()

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
        print(f'Player {self.getPlayerPosition(PlayerType.CURRENT)}')
        print(f'Enemy {self.getPlayerPosition(PlayerType.ENEMY)}')
        nextPotentialPositions = self.getNextPotentialPositions()
        print(nextPotentialPositions)

    def getNextPotentialPositions(self):
        self.playerPosition = self.getPlayerPosition(PlayerType.CURRENT)
        xPos, yPos = self.playerPosition[0], self.playerPosition[1]
        #Get the board
        #comparer les valeurs, sachant que xPos et yPos représentent les indices pas les valeurs
        nextPosition = []
        board = self.board
        if self.current == 1:
            if board[xPos - 1][yPos] == 3:
                nextPosition.append((xPos - 2, yPos))
            if board[xPos + 1][yPos] == 3:
                nextPosition.append((xPos + 2, yPos))
            if board[xPos][yPos - 1] == 3:
                nextPosition.append((xPos, yPos - 2))
            if board[xPos][yPos + 1] == 3:
                nextPosition.append((xPos, yPos + 2))
        
        elif self.current == 0:
            if board[xPos + 1][yPos] == 3:
                nextPosition.append((xPos + 2, yPos))
            if board[xPos - 1][yPos] == 3:
                nextPosition.append((xPos - 2, yPos))
            if board[xPos][yPos - 1] == 3:
                nextPosition.append((xPos, yPos - 2))
            if board[xPos][yPos + 1] == 3:
                nextPosition.append((xPos, yPos + 2))
        return nextPosition

        
    def getAvailableMove(self):
        pass

    def isPieceOccupied(self):
        pass

    def isWallOccupied(self):
        pass

    def __str__(self):
      return f"My state is {self.lives}"