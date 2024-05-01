class Game:
    def __init__(self, lives, errors, state, players, current, blockers, board):
        self.lives = lives
        self.errors = errors
        self.state = state
        self.players = players
        self.current = current
        self.blockers = blockers
        self.board = board

    def setState(self, request):
        self.state = request['state']
        self.players = self.state['players']
        self.current = self.state['current']
        self.blockers = self.state['blockers']
        self.board = self.board['board']

class State:
    def __init__(self, isSimulation = False):
        self.isSimulation = isSimulation