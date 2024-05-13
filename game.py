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
        jokeList = ['Prends ça!', "Mdrrrr, même pas mal", 'Croûte', 'Bim bam boum', 'Wesh alors', 
                    'Par la barbe de Merlin', 'Saperlipopette', 'Bisous, je m anvole']
        
        potential_moves = self.getNextPotentialPositions()
        potential_blocks = self.blockersPlacements() if self.blockers[self.current] > 0 else []

        print("Potential moves:", potential_moves)
        print("Potential blocks:", potential_blocks)

        if not potential_moves and not potential_blocks:
            return json.dumps({"response": "pass", "message": "No moves available."})

        actions = []
        if potential_moves:
            actions.append(("move", random.choice(potential_moves)))
        if potential_blocks:
            actions.append(("block", random.choice(potential_blocks)))

        action_type, position = random.choice(actions) if actions else (None, None)

        if action_type == 'move':
            moveType = {"type": "pawn", "position": [position]}
            print(f'Moving to: {position}')
        elif action_type == 'block':
            moveType = {"type": "blocker", "position": position}
            print(f'Placing blocker at: {position}')
        else:
            return json.dumps({"response": "pass", "message": "No moves available."})

        message = random.choice(jokeList)
        request = {
            "response": "move",
            "move": moveType,
            "message": message
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
            (0, 1),  # Right
            (0, -1)  # Left
        ]

        for dx, dy in directions:
            target_x, target_y = xPos + 2 * dx, yPos + 2 * dy
            blocker_x, blocker_y = xPos + dx, yPos + dy

            if 0 <= blocker_x < rows and 0 <= blocker_y < cols and \
            0 <= target_x < rows and 0 <= target_y < cols:
                if board[blocker_x][blocker_y] == 3 and board[target_x][target_y] == 2:
                    nextPositions.append([target_x, target_y])

        return nextPositions

    def getPotentialBlockersPlacements(self):
        freePlaces = []
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if item == 3:  # Assuming 3 denotes a valid place for a blocker
                    freePlaces.append((i, j))
        print("Free places for blockers:", freePlaces)
        return freePlaces

    def isHorizontalBlockPossible(self, x, y, freePlaces):
        return (x, y+1) in freePlaces

    def isVerticalBlockPossible(self, x, y, freePlaces):
        return (x+1, y) in freePlaces


    def blockersPlacements(self):
        placement = []
        freePlaces = self.getPotentialBlockersPlacements()
        rows, cols = len(self.board), len(self.board[0])

        print(f"Free places: {sorted(freePlaces)}")

        for x, y in sorted(freePlaces):
            # Check horizontal direct adjacency
            if y + 1 < cols:
                if self.isHorizontalBlockPossible(x, y, freePlaces):
                    placement.append([(x, y), (x, y + 1)])
                    print(f"Horizontal placement added: {(x, y)} to {(x, y + 1)}")

            # Check vertical direct adjacency
            if x + 1 < rows:
                if self.isVerticalBlockPossible(x, y, freePlaces):
                    placement.append([(x, y), (x + 1, y)])
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

        actions = self.all_actions()  

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
                break  

        return bestValue, bestSequence


    
    
    
    