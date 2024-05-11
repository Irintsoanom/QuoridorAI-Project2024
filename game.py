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
        print(f'Potential next position : {nextPotentialPositions}')
        print(self.getPotentialBlockersPlacements())
        print(self.blockersPlacements())

    def getNextPotentialPositions(self):
        self.playerPosition = self.getPlayerPosition(PlayerType.CURRENT)
        xPos, yPos = self.playerPosition[0], self.playerPosition[1]
        nextPosition = []
        board = self.board
        if self.current == 1:
            if board[xPos - 1][yPos] == 3:
                nextPosition.append((xPos - 2, yPos))
            if board[xPos + 1][yPos] == 3:
                nextPosition.append((xPos + 2, yPos))
            if board[xPos + 2][yPos] == 1:
                nextPosition.append((xPos + 4, yPos))
            if board[xPos][yPos - 1] == 3:
                nextPosition.append((xPos, yPos - 2))
            if board[xPos][yPos + 1] == 3:
                nextPosition.append((xPos, yPos + 2))
        
        elif self.current == 0:
            if board[xPos + 1][yPos] == 3:
                nextPosition.append((xPos + 2, yPos))
            if board[xPos - 1][yPos] == 3:
                nextPosition.append((xPos - 2, yPos))
            if board[xPos - 2][yPos] == 1:
                nextPosition.append((xPos - 4, yPos))
            if board[xPos][yPos - 1] == 3:
                nextPosition.append((xPos, yPos - 2))
            if board[xPos][yPos + 1] == 3:
                nextPosition.append((xPos, yPos + 2))
        return nextPosition
    
    def getPotentialBlockersPlacements(self):
        freePlaces = []
        for i, list in enumerate(self.board):
            for j, item in enumerate(list):
                if item == 3:
                    freePlaces.append((i, j))
        return freePlaces
    
    def blockersPlacements(self):
        placement = []
        freePlaces = self.getPotentialBlockersPlacements()
        for elem in freePlaces:
            x, y = elem[0], elem[1]
            #Perpendiculaire non réglé A CORRIGER ABSOLUMENT
            if (x, y+2) in freePlaces and (x-1, y+1) in freePlaces and (x+1, y+1) in freePlaces:
                placement.append([(x, y), (x, y+2)])
            if (x+2, y) in freePlaces and (x+1, y-1) in freePlaces and (x+1, y+1) in freePlaces:
                placement.append([(x,y), (x+2, y)]) 
        return placement

    def positionFeature(self):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT)
        positionMapping = {16:0, 14:2, 12:4, 10:6, 8:8, 6:10, 4:12, 2:14, 0:16}
        if self.current == 0:
            return playerPosition[0]
        else:
            return positionMapping.get(playerPosition[0], None)

    def positionDifference(self):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT)
        enemyPosition = self.getPlayerPosition(PlayerType.ENEMY)
        diff = abs(playerPosition[0]- enemyPosition[0])
        return diff
    
    def movesToNextColumn(self):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT)
        xPos = playerPosition[0]
        yPos = playerPosition[1]
        board = self.board
        yLeft = yPos
        yRight = yPos
        while board[xPos + 1] == 4:
            yLeft -= 1
            yRight += 1
        xPos += 1
        return (xPos, min(yLeft, yRight))

    