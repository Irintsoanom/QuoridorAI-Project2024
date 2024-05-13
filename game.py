from enum import Enum
import math
import copy
import json

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
        moveType = None
        jokeList = ['Prends ça!', "Mdrrrr, même pas mal", 'Croûte', 'Bim bam boum', 'Wesh alors', 'Par la barbe de Merlin', 'Saperlipopette', 'Bisous, je m anvole']
        move = self.bestMove()
        block = self.bestBlockerPosition()
        print('here')
        print(move)
        print(block)
        best = max(move[1], block[1])
        if best in move:
            moveType = {
                "type" : "pawn",
                "position": [move[0]]
            }
        elif best in block:
            moveType = {
                "type" : "blocker",
                "position": block[0]
            }
        request = {
                "response": "move",
                "move": moveType,
                "message": "Fun message"
                }
        message = json.dumps(request)
        return message

    def getNextPotentialPositions(self):
        self.playerPosition = self.getPlayerPosition(PlayerType.CURRENT, self.board)
        xPos, yPos = self.playerPosition[0], self.playerPosition[1]
        nextPosition = []
        board = self.board
        rows, cols = len(board), len(board[0])

        def isMovePossible(x, y, stepX, stepY, conditionVal):
            newX, newY = x + stepX, y + stepY
            if 0 <= newX < rows and 0 <= newY < cols and board[newX][newY] == conditionVal:
                return True
            return False
        
        if self.current == 1:
            if isMovePossible(xPos, yPos, -1, 0, 3):
                nextPosition.append([xPos - 2, yPos])
            if isMovePossible(xPos, yPos, 1, 0, 3):
                nextPosition.append([xPos + 2, yPos])
            if isMovePossible(xPos, yPos, 2, 0, 0):
                nextPosition.append([xPos + 4, yPos])
            if isMovePossible(xPos, yPos, 0, -1, 3):
                nextPosition.append([xPos, yPos - 2])
            if isMovePossible(xPos, yPos, 0, 1, 3):
                nextPosition.append([xPos, yPos + 2])

        elif self.current == 0:
            if isMovePossible(xPos, yPos, 1, 0, 3):
                nextPosition.append([xPos + 2, yPos])
            if isMovePossible(xPos, yPos, -1, 0, 3):
                nextPosition.append([xPos - 2, yPos])
            if isMovePossible(xPos, yPos, -2, 0, 1):
                nextPosition.append([xPos - 4, yPos])
            if isMovePossible(xPos, yPos, 0, -1, 3):
                nextPosition.append([xPos, yPos - 2])
            if isMovePossible(xPos, yPos, 0, 1, 3):
                nextPosition.append([xPos, yPos + 2])

        print(nextPosition)
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
            try:
                # Horizontal
                if ((x, y+2) in freePlaces and (x-1, y+1) in freePlaces and (x+1, y+1) in freePlaces) or ((x, y+2) in freePlaces and (x+1, y+1) in freePlaces and (x-1, y+1) not in freePlaces and (x-3, y+1) not in freePlaces) or ((x, y+2) in freePlaces and (x-1, y+1) in freePlaces and (x+1, y+1) not in freePlaces and (x+3, y+1) not in freePlaces) or ((x, y+2) in freePlaces and (x-1, y+1) not in freePlaces and (x-3, y+1) not in freePlaces and (x+1, y+1) not in freePlaces and (x+3, y+1 not in freePlaces)):
                    placement.append([[x, y], [x, y+2]])
                # Vertical 
                if ((x+2, y) in freePlaces and (x+1, y+1) in freePlaces and (x+1, y-1) in freePlaces) or ((x+2, y) in freePlaces and (x+1, y-1) in freePlaces and (x+1, y+1) not in freePlaces and (x+1, y+3) not in freePlaces) or ((x+2, y) in freePlaces and (x+1,y+1) in freePlaces and (x+1, y-1) not in freePlaces and (x+1, y-3) not in freePlaces) or ((x+2, y) in freePlaces and (x+1, y+1) not in freePlaces and (x+1, y+3) not in freePlaces and (x+1, y-1) not in freePlaces and (x+1, y-3) not in freePlaces):
                    placement.append([[x,y], [x+2, y]]) 
            except:
                None
        return placement
    
    def simulateMove(self, move):
        mockBoard = copy.deepcopy(self.board)
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        x, y = playerPosition[0], playerPosition[1]
        newX, newY = move[0], move[1]
        mockBoard[x][y] = 2
        mockBoard[newX][newY] = self.current
        return self.evaluate(mockBoard, 3, 4, 5)
    
    def simulateBlocking(self, position):
        mockBoard = copy.deepcopy(self.board)
        for elem in position:
            newX = elem[0]
            newY = elem[1]
            mockBoard[newX][newY] = 4
        return self.evaluate(mockBoard, 2, 1, 1)

        
    def positionFeature(self, mockBoard):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        positionMapping = {16:0, 14:2, 12:4, 10:6, 8:8, 6:10, 4:12, 2:14, 0:16}
        if self.current == 0:
            return playerPosition[0]
        else:
            return positionMapping.get(playerPosition[0], None)

    def positionDifference(self, mockBoard):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        enemyPosition = self.getPlayerPosition(PlayerType.ENEMY, mockBoard)
        try:
            diff = abs(playerPosition[0] - enemyPosition[0])
            return diff
        except:
            return 0
    
    def movesToNextColumn(self, mockBoard):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        xPos = playerPosition[0]
        yPos = playerPosition[1]
        yLeft = yPos
        yRight = yPos

        try:
            while True:
                if 0 < yLeft and mockBoard[xPos + 1][yLeft] == 4:
                    yLeft -= 1
                elif  yRight and mockBoard[xPos + 1][yRight] == 4:
                    yLeft += 1
                else:
                    break

            if abs(yLeft - yPos) <= abs(yRight - yPos):
                yOptimum = yLeft
            else:
                yOptimum = yRight
            return yOptimum - yPos
        except IndexError:
            return 0
        
    def evaluate(self, mockBoard):
        positionFeature = self.positionFeature(mockBoard)
        positionDiff = self.positionDifference(mockBoard)
        moveToNext = self.movesToNextColumn(mockBoard)
        return positionFeature + positionDiff + moveToNext
    
    def bestMove(self):
        bestScore = -math.inf
        bestMove = None
        print('best positions')
        print(self.getNextPotentialPositions())
        for position in self.getNextPotentialPositions():
            print('position')
            print(position)
            score = self.simulateMove(position)
            if score > bestScore:
                bestMove = position
                bestScore = score
                return [bestMove, bestScore]

    def bestBlockerPosition(self):
        bestScore = -math.inf
        bestBlockersPlacement = None
        myBlockers = self.blockers[self.current]
        if myBlockers > 0:
            for emptyPlaces in self.blockersPlacements():
                score = self.simulateBlocking(emptyPlaces)
                if score > bestScore:
                    bestBlockersPlacement = emptyPlaces
                    bestScore = score
                    return [bestBlockersPlacement, bestScore]
        else:
            return [None, -math.inf]
            
    
    # def minimax(self, board, depth, maximizingPlayer):
    #     if depth == 0:
    #         return self.evaluate(board)
        
    #     if maximizingPlayer:
    #         maxEval = -math.inf
    #         for position in self.getNextPotentialPositions():
    #             newBoard = self.simulateMove(position)
    #             eval = self.minimax(newBoard, depth - 1, False)
    #             maxEval = max(maxEval, eval)
    #         return maxEval
    #     else:
    #         minEval = math.inf
    #         for position in self.getNextPotentialPositions():
    #             newBoard = self.simulateMove(position)
    #             eval = self.minimax(newBoard, depth - 1, True)
    #             minEval = min(minEval, eval)
    #         return minEval
    
    