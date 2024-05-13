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
        bestValue, bestSequence = self.minimax(2, True)

        firstAction = bestSequence[0]
        actionType, position = firstAction[0], firstAction[1]
        print(f'Blockers : {self.blockersPlacements()}')

        if actionType == 'move':
            print(f'pawn:  {position}')
            moveType = {"type": "pawn", "position": [position]}
        else:
            print(f'Block:  {position}')
            moveType = {"type": "blocker", "position": position}

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


    def getPotentialBlockersPlacements(self):
        freePlaces = set()
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if item == 3:  
                    freePlaces.add((i, j))
        return freePlaces
    
    def isHorizontalBlockPossible(self, x, y, freePlaces):
        isHorizontalPossible = (x, y+2) in freePlaces
        check1 = (x-1, y+1) in freePlaces
        check2 = (x+1, y+1) in freePlaces
        check3 = (x-3, y+1) not in freePlaces
        check4 = (x+3, y+1) not in freePlaces

        if isHorizontalPossible:
            condition1 = check1 and check2
            condition2 = (check2 and check3) or (check1 and check4) 
            condition3 = not check1 and check3 and not check2 and check4

            return condition1 or condition2 or condition3
        return False
    
    def isVerticalBlockPossible(self, x, y, freePlaces):
        isVerticalPossible = (x+2, y) in freePlaces
        check1 = (x+1, y+1) in freePlaces
        check2 = (x+1, y-1) in freePlaces
        check3 = (x+1, y+3) not in freePlaces
        check4 = (x+1, y-3) not in freePlaces

        if isVerticalPossible:
            condition1 = check1 and check2  # Both (x+1, y+1) and (x+1, y-1) must be in freePlaces
            condition2 = (check2 and not check1 and check3)  # (x+1, y-1) in and (x+1, y+1) not in freePlaces, and (x+1, y+3) not in freePlaces
            condition3 = (check1 and not check2 and check4)  # (x+1, y+1) in and (x+1, y-1) not in freePlaces, and (x+1, y-3) not in freePlaces
            condition4 = not check1 and check3 and not check2 and check4  # Neither (x+1, y+1) nor (x+1, y-1) in freePlaces, and both (x+1, y+3) and (x+1, y-3) not in freePlaces

            return condition1 or condition2 or condition3 or condition4
        return False

    def blockersPlacements(self):
        placement = []
        freePlaces = self.getPotentialBlockersPlacements()
        rows, cols = len(self.board), len(self.board[0])

        print(f"Free places: {sorted(freePlaces)}")  # Sorted for easier reading

        for x, y in sorted(freePlaces):
            # Horizontal check
            if y + 2 < cols:
                horizontal_check = all(self.board[x][y + offset] == 3 for offset in range(2))
                if horizontal_check:
                    placement.append([(x, y), (x, y + 2)])
                    print(f"Horizontal placement added: {(x, y)} to {(x, y + 2)}")

            # Vertical check
            if x + 2 < rows:
                vertical_check = all(self.board[x + offset][y] == 3 for offset in range(2))
                if vertical_check:
                    placement.append([(x, y), (x + 2, y)])
                    print(f"Vertical placement added: {(x, y)} to {(x + 2, y)}")

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
        print(f'Blockers : {position}')
        for elem in position:
            newX = elem[0]
            newY = elem[1]
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


    
    
    
    