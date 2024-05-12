from enum import Enum
import math
import copy

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
    
    def getPlayerPosition(self, playerType: PlayerType, board):
        player = self.current if playerType == PlayerType.CURRENT else self.enemy
        for i, list in enumerate(board):
            for j, item in enumerate(list):
                if item == player:
                    return (i, j)
        return (None, None)
    
    def play(self):
        move = self.bestMove()
        block = self.bestBlockerPosition()
        best = max(move[0], block[0])
        if best in move:
            #envoyer l'instruction move
            pass
        elif best in block:
            pass

    def getNextPotentialPositions(self):
        self.playerPosition = self.getPlayerPosition(PlayerType.CURRENT, self.board)
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
    
    def simulateMove(self, move):
        mockBoard = copy.deepcopy(self.board)
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        x, y = playerPosition[0], playerPosition[1]
        newX, newY = move[0], move[1]
        mockBoard[x][y] = 2
        print(f'{newX} et y : {newY}')
        mockBoard[newX][newY] = self.current
        return self.evaluate(move, mockBoard)
    
    def simulateBlocking(self, position):
        mockBoard = copy.deepcopy(self.board)
        for elem in position:
            first = elem[0]
            second = elem[1]
            a, b = first[0], first[1]
            c, d = second[0], second[1]
            mockBoard[a][b] = 4
            mockBoard[c][d] = 4
            return self.evaluate(position, mockBoard)

        
    def positionFeature(self, move, mockBoard):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        positionMapping = {16:0, 14:2, 12:4, 10:6, 8:8, 6:10, 4:12, 2:14, 0:16}
        if self.current == 0:
            return playerPosition[0]
        else:
            return positionMapping.get(playerPosition[0], None)

    def positionDifference(self, move, mockBoard):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        enemyPosition = self.getPlayerPosition(PlayerType.ENEMY, mockBoard)
        diff = abs(playerPosition[0] - enemyPosition[0])
        print(f'player : {playerPosition}, Enemy : {enemyPosition}')
        return diff
    
    def movesToNextColumn(self, move, mockBoard):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        xPos = playerPosition[0]
        yPos = playerPosition[1]
        yLeft = yPos
        yRight = yPos
        while mockBoard[xPos + 1] == 4 and 0 < yLeft < 17 and 0 < yRight < 17:
            yLeft -= 1
            yRight += 1
        xPos += 1
        yOptimum = min(yLeft, yRight)
        return [(xPos, yOptimum), yOptimum - yPos]
        
    def evaluate(self, move, mockBoard):
        positionFeature = self.positionFeature(move)
        positionDiff = self.positionDifference(move)
        moveToNext = self.movesToNextColumn(move)
        return positionFeature + positionDiff + moveToNext[1]
    
    def bestMove(self):
        bestScore = -math.inf
        bestMove = None
        for position in self.getNextPotentialPositions():
            score = self.simulateMove(position)
            if score > bestScore:
                bestMove = position
                bestScore = score
                return [bestMove, bestScore]

    def bestBlockerPosition(self):
        bestScore = -math.inf
        bestBlockersPlacement = None
        if self.blockers > 0:
            for emptyPlaces in self.blockersPlacements():
                score = self.simulateBlocking(emptyPlaces)
                if score > bestScore:
                    bestMove = emptyPlaces
                    bestScore = score
                    return [bestMove, bestScore]
        else:
            return [None, -math.inf]
            
    
    def minimax(self, board, depth, maximizingPlayer):
        if depth == 0:
            return self.evaluate(board)
        
        if maximizingPlayer:
            maxEval = -math.inf
            for position in self.getNextPotentialPositions():
                newBoard = self.simulateMove(position)
                eval = self.minimax(newBoard, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = math.inf
            for position in self.getNextPotentialPositions():
                newBoard = self.simulateMove(position)
                eval = self.minimax(newBoard, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval
    
    