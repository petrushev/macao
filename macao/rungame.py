from macao.strategies import Human, RandomAi
from macao import Game

def main():
    #g = Game(methods =[Human, RandomAi, RandomAi, RandomAi, RandomAi, RandomAi])
    g = Game(methods =[Human, RandomAi])
    #print g.players[0], '\t', g.players[0]
    #print '--', g.ground,'--'
    while not g.finished:
        g.do_turn()

if __name__=='__main__':
    main()
