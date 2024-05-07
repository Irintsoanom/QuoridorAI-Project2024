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

    #get the potential place where I can put the walls
    #free places are represented by 3 - 5 - 3, occupied places are represented by 4
    #walls can't completely block any of the players -> How can i check??
    #a wall can be horizontal or vertical and take 2 places 3 - 5 - 3
    #Comment ?
    #chercher les positions dans le tableau 3
    #vérifier si le schéma 3 - 5 - 3 est réspecté
    #si l'index en y de 3 est paire alors vérifier si index + 2 = 3 aussi alors dans ce cas la place est libre
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
            if (x, y+2) in freePlaces:
                placement.append([(x, y), (x, y+2)])
            if (x+2, y) in freePlaces:
                placement.append([(x,y), (x+2, y)]) 
        return placement
        
    #for elem in freePlaces:
    #x = elem[0] et y = elem[1]
    #if (x, y + 2) in list
    #Place.append([(x,y), (x, y + 2)])

    #faire une fonction eval qui calcule la distance qui sépare du côté opposé
    def getAvailableMove(self):
        pass

    def isPieceOccupied(self):
        pass

    def isWallOccupied(self):
        pass

    def __str__(self):
      return f"My state is {self.lives}"