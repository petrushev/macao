from macao.strategies import Human, RandomAi
from macao import Game

def main():
    #g = Game(methods = [Human, RandomAi])
    #g = Game(methods = [Human, Human])
    g = Game(methods = [Human, RandomAi, RandomAi, RandomAi])
    while not g.finished:
        g.do_turn()

if __name__=='__main__':
    main()
