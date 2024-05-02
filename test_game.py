from game import Game

gs = Game()
#Si current == 0 et position = (0, 8) alors
#La sortie devrait être [(2,8), (0,6), (0,10)]

def test_getNextPotentialPositions():
    if gs.current == 0 and gs.playerPosition == (0, 8):
        assert gs.getNextPotentialPositions() == [(2,8), (0,6), (0,10)] 