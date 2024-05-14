from game import Game, PlayerType
import pytest

gs = Game()
#Si current == 0 et position = (0, 8) alors
#La sortie devrait être [(2,8), (0,6), (0,10)]

def test_getNextPotentialPositions():
    if gs.current == 0 and gs.playerPosition == (2, 8):
        assert gs.getNextPotentialPositions() == [(10,8), (0,8), (2,6), (2,10)] 

def test_positionFeature():
    playerPosition = (2,8)
    if gs.current == 0:
        result = gs.positionFeature()
        assert gs.positionFeature() == result

def test_positionDifference():
    pass

# Sample board setup for testing
initial_board = [
    [0, 2, 2, 2, 0],
    [2, 2, 2, 2, 2],
    [2, 2, 1, 2, 2],
    [2, 2, 2, 2, 2],
    [0, 2, 2, 2, 0]
]

@pytest.fixture
def game():
    g = Game()
    g.board = initial_board.copy()
    g.current = 0  # Assume player 1 starts
    g.enemy = 1
    return g

def test_initialization(game):
    assert game.lives == 3
    assert game.current == 0
    assert game.enemy == 1
    assert game.blockers == [10, 10]

def test_set_state(game):
    message = {
        'state': {
            'board': initial_board,
            'current': 1,
            'blockers': [9, 10]
        },
        'lives': 2,
        'errors': None
    }
    game.setState(message)
    assert game.lives == 2
    assert game.current == 1
    assert game.board == initial_board
    assert game.blockers == [9, 10]

def test_get_player_position(game):
    pos = game.getPlayerPosition(PlayerType.CURRENT, game.board)
    assert pos == (2, 2)

def test_get_next_potential_positions(game):
    game.current = 0  
    possible_moves = game.getNextPotentialPositions()
    expected_moves = [[0, 2], [4, 2], [2, 0], [2, 4]]  
    assert sorted(possible_moves) == sorted(expected_moves)

def test_blocker_placements(game):
    blockers = game.blockersPlacements()
    expected_blockers = [([(1, 1), (1, 3)]), ([(3, 1), (3, 3)])] 
    assert sorted(blockers) == sorted(expected_blockers)

def test_minimax(game):
    value, moves = game.minimax(1, True)
    assert type(value) is float
    assert type(moves) is list

