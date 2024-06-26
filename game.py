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
        self.moveCount = 0

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
    
    def log_state(self):
        print(f"Current board state: {self.board}")
        print(f"Current player: {self.current}, Enemy player: {self.enemy}")
        print(f"Available blockers: {self.blockers}")
        print(f"Move count: {self.moveCount}")

    def play(self):
        self.log_state()
        jokeList = ['Prends ça!', "Mdrrrr, même pas mal", 'Croûte', 'Bim bam boum',
                'Wesh alors', 'Par la barbe de Merlin', 'Saperlipopette', 'Bisous, je m envole']
        try:
            if self.moveCount % 5 == 0 and self.moveCount > 0:
                print("Checking for blocker placement...")
                potentialBlocks = self.blockersPlacements()
                if potentialBlocks:
                    chosenBlock = random.choice(potentialBlocks)
                    print(f"Placing blocker at: {chosenBlock}")
                    moveType = {"type": "blocker", "position": chosenBlock}
                    self.moveCount += 1
                    return json.dumps({
                        "response": "move",
                        "move": moveType,
                        "message": random.choice(jokeList)
                    })
                else:
                    print("No valid places for blockers.")

            print("Calculating pawn move...")
            bestValue, bestSequence = self.minimax(1, True)
            if bestSequence:
                firstAction = bestSequence[0]
                moveType = {"type": "pawn", "position": [firstAction]}
                self.moveCount += 1
                print(f"Pawn move decided: {firstAction}")
            else:
                print("No valid moves available, passing turn.")
                return json.dumps({"response": "pass"})
        except:
            print('Time out')

        request = {
            "response": "move",
            "move": moveType,
            "message": random.choice(jokeList)
        }
        return json.dumps(request)

    def getNextPotentialPositions(self):
        self.playerPosition = self.getPlayerPosition(PlayerType.CURRENT, self.board)
        if self.playerPosition == (None, None):
            print("Player position not found.")
            return []

        xPos, yPos = self.playerPosition
        nextPositions = []
        board = self.board
        rows, cols = len(board), len(board[0])

        directions = [
            (1, 0) if self.current == 0 else (-1, 0),
            (0, 1),  
            (0, -1)  
        ]

        for dx, dy in directions:
            target_x, target_y = xPos + 2 * dx, yPos + 2 * dy
            blocker_x, blocker_y = xPos + dx, yPos + dy

            if 0 <= blocker_x < rows and 0 <= blocker_y < cols and \
            0 <= target_x < rows and 0 <= target_y < cols:
                if board[blocker_x][blocker_y] == 3 and board[target_x][target_y] == 2:
                    nextPositions.append([target_x, target_y])

        return nextPositions

    def getPotentialBlockersPlacements(self, itemNumber):
        freePlaces = []
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if item == itemNumber:  
                    freePlaces.append((i, j))
        return freePlaces
    
    def blockersPlacements(self):
        placement = []
        freePlaces = self.getPotentialBlockersPlacements(3)
        pawnPlaces = self.getPotentialBlockersPlacements(2)

        print(f'All available : {freePlaces}')
        for elem in freePlaces:
            x, y = elem[0], elem[1]
            if (x,y + 2) in freePlaces and (x, y+1) not in pawnPlaces:
                    placement.append([(x, y), (x, y + 2)])
                    print(f"Horizontal placement added: {(x, y)} to {(x, y + 2)}")
            if (x + 2, y) in freePlaces and (x+1, y) not in pawnPlaces:
                    placement.append([(x, y), (x + 2, y)])
                    print(f"Vertical placement added: {(x, y)} to {(x + 1, y)}")
        print(f"Computed placements: {placement}")
        return placement

    def simulateMove(self,mockBoard, move):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        x, y = playerPosition[0], playerPosition[1]
        newX, newY = move[0], move[1]
        mockBoard[x][y] = 2
        mockBoard[newX][newY] = self.current
        return self.evaluate(mockBoard)
        
    def positionFeature(self, mockBoard):
        playerPosition = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        positionMapping = {16:0, 14:2, 12:4, 10:6, 8:8, 6:10, 4:12, 2:14, 0:16}
        if self.current == 0:
            return playerPosition[0]
        else:
            return positionMapping.get(playerPosition[0], None)

    def positionDifference(self, mockBoard):
        playerPos = self.getPlayerPosition(PlayerType.CURRENT, mockBoard)
        enemyPos = self.getPlayerPosition(PlayerType.ENEMY, mockBoard)
        score = 0
        board_size = len(mockBoard) 

        if self.current == 0:
            score += playerPos[0]
        else:
            score += (board_size - playerPos[0]) 

        score -= abs(playerPos[0] - enemyPos[0]) / board_size  

        return score
    
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

    def minimax(self, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
        if depth == 0:
            return self.evaluate(self.board), []

        if maximizingPlayer:
            maxEval = float('-inf')
            best_sequence = []
            for move in self.getNextPotentialPositions():
                newBoard = copy.deepcopy(self.board)
                eval = self.simulateMove(newBoard, move)  # Evaluate the move
                _, sequence = self.minimax(depth - 1, False, alpha, beta)
                if eval > maxEval:
                    maxEval = eval
                    best_sequence = [move] + sequence
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            return maxEval, best_sequence
        else:
            minEval = float('inf')
            best_sequence = []
            for move in self.getNextPotentialPositions():
                newBoard = copy.deepcopy(self.board)
                eval = self.simulateMove(newBoard, move)  # Evaluate the move
                _, sequence = self.minimax(depth - 1, True, alpha, beta)
                if eval < minEval:
                    minEval = eval
                    best_sequence = [move] + sequence
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            return minEval, best_sequence




    
    
    
    