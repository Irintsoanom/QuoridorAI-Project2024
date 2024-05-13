from enum import Enum
import math
import copy
import json
import random

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
        bestValue, bestSequence = self.minimax(1, True)

        firstAction = bestSequence[0]
        actionType, position = firstAction[0], firstAction[1]

        if actionType == 'move':
            moveType = {"type": "pawn", "position": position}
        else:
            moveType = {"type": "blocker", "position": position}

        request = {
            "response": "move",
            "move": moveType,
            "message": random.choice(jokeList)
        }

        return json.dumps(request)

    def getNextPotentialPositions(self):
        self.playerPosition = self.getPlayerPosition(PlayerType.CURRENT, self.board)
        if not self.playerPosition:
            print("Player position not found.")
            return []

        xPos, yPos = self.playerPosition
        nextPositions = []
        board = self.board
        rows, cols = len(board), len(board[0])

        moves = [(-1, 0), (1, 0), (-2, 0), (0, -1), (0, 1)]
        for dx, dy in moves:
            newX, newY = xPos + dx, yPos + dy
            if 0 <= newX < rows and 0 <= newY < cols:
                if board[newX][newY] == 3 or (dx == -2 and board[newX][newY] == 1):
                    nextPositions.append([newX, newY])
                elif dx == 2 and newY == 0 and board[newX][newY] == 3:  # Specific condition
                    nextPositions.append([newX, newY])

        print(f'Next positions: {nextPositions}')
        return nextPositions
    
    def getPotentialBlockersPlacements(self):
        freePlaces = set()
        for i, list in enumerate(self.board):
            for j, item in enumerate(list):
                if item == 3:
                    freePlaces.add((i, j))
        return freePlaces
    
    def blockersPlacements(self):
        placement = []
        freePlaces = self.getPotentialBlockersPlacements()
        placement = []
        freePlaces = self.getPotentialBlockersPlacements()
        for x, y in freePlaces:
            # Horizontal check
            if all([(x, y + offset) in freePlaces for offset in [1, 2]]):
                placement.append([[x, y], [x, y + 2]])
            # Vertical check
            if all([(x + offset, y) in freePlaces for offset in [1, 2]]):
                placement.append([[x, y], [x + 2, y]])
        return placement
    
    def simulateMove(self,mockBoard, move):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        x, y = playerPosition[0], playerPosition[1]
        newX, newY = move[0], move[1]
        mockBoard[x][y] = 2
        mockBoard[newX][newY] = self.current
        return self.evaluate(mockBoard)
    
    def simulateBlocking(self,mockBoard, position):
        newX = position[0]
        newY = position[1]
        mockBoard[newX][newY] = 4
        return self.evaluate(mockBoard)

        
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
    
    # def minimax(self, depth, maximizingPlayer, alpha = float('-inf'), beta = float('inf')):
    #     if depth == 0:
    #         return self.evaluate(self.board), []
        
    #     bestValue = -math.inf if maximizingPlayer else math.inf
    #     bestSequence = []

    #     potentialMoves = self.getNextPotentialPositions()
    #     potentialBlocks = self.getPotentialBlockersPlacements() if self.blockers[self.current] > 0 else []


    #     actions = [('move', move) for move in potentialMoves] + [('block', block) for block in potentialBlocks]

    #     for actionType, action in actions:
    #         newBoard = copy.deepcopy(self.board)
    #         if actionType == 'move':
    #             self.simulateMove(newBoard, action)
    #         else:
    #             self.simulateBlocking(newBoard, action)

    #         eval, sequence = self.minimax(depth-1, not maximizingPlayer, alpha, beta)

    #         if maximizingPlayer:
    #             if eval > bestValue:
    #                 bestValue = eval
    #                 bestSequence = [action] + sequence
    #             alpha = max(alpha, eval)
    #         else:
    #             if eval < bestValue:
    #                 bestValue = eval
    #                 bestSequence = [action] + sequence
    #             beta = min(beta, eval)

    #         if beta <= alpha:
    #             break
    #     return bestValue, bestSequence

    def all_actions(self):
        move_actions = [('move', move) for move in self.getNextPotentialPositions()]
        
        blocker_actions = []
        if self.blockers[self.current] > 0:  
            blocker_actions = [('block', block) for block in self.blockersPlacements()]
        
        return move_actions + blocker_actions


    def minimax(self, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
        if depth == 0:
            return self.evaluate(self.board), []

        bestValue = float('-inf') if maximizingPlayer else float('inf')
        bestSequence = []

        actions = self.all_actions()  # Get all actions from the new method

        for actionType, action in actions:
            newBoard = copy.deepcopy(self.board)
            if actionType == 'move':
                self.simulateMove(newBoard, action)
            else:
                self.simulateBlocking(newBoard, action)

            eval, sequence = self.minimax(depth - 1, not maximizingPlayer, alpha, beta)

            if maximizingPlayer:
                if eval > bestValue:
                    bestValue = eval
                    bestSequence = [(actionType, action)] + sequence
                alpha = max(alpha, eval)
            else:
                if eval < bestValue:
                    bestValue = eval
                    bestSequence = [(actionType, action)] + sequence
                beta = min(beta, eval)

            if beta <= alpha:
                break  # Alpha-beta pruning

        return bestValue, bestSequence


    
    
    
    