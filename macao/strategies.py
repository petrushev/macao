from random import choice, random

from macao import can_play, SUITES

class Strategy(object):
    def __init__(self, player):
        self.player = player

    def draw(self):
        self.player.draw()

class Human(Strategy):

    def play(self):
        player = self.player
        hand = list(player.hand)

        print ' '.join(hand).encode('utf-8'),' | ', player.game.ground.encode('utf-8')

        # enter valid card for playing, 0 for draw
        ord_ = '-1'
        while not(ord_.isdigit()) or int(ord_) < 0 or int(ord_) > len(hand):
            ord_ = raw_input()
            ord_ = ord_.strip()
        ord_ = int(ord_)

        if ord_ == 0:
            return None, None

        played = hand[ord_ - 1]
        wanted_suite = None # only applicable for 'J's

        if played[0] == 'J':
            ord_ = '0'
            while not(ord_.isdigit()) or int(ord_) < 1 or int(ord_) > 4:
                ord_ = raw_input(' '.join(tuple(SUITES)).encode('utf-8')+' : ')
                ord_ = ord_.strip()
            wanted_suite= SUITES[int(ord_) - 1]

        return played, wanted_suite

class RandomAi(Strategy):

    def play(self):
        player = self.player
        hand = list(player.hand)
        ground = player.game.ground

        possibles = [h for h in hand if can_play(h, ground)]
        if random() < .15:
            possibles.append(0) # possibly bluff for new card
        played = choice(possibles)

        if played == 0:
            return None, None

        if played[0]=='J':
            # laplace smoothed for random suites
            choices = [h[-1] for h in hand
                             if h[:-1]!='J']
            choices.extend(SUITES)
            wanted_suite = choice(choices)

        else:
            wanted_suite = None

        return played, wanted_suite
