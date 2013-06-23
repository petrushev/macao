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

class AugmentedAi(Strategy):

    def play(self):
        player = self.player
        hand = list(player.hand)
        ground = player.game.ground
        pushed_7 = player.game.pushed_7

        possibles = [h for h in hand if can_play(h, ground)]
        possible_heads = [h[:-1] for h in possibles]


        # play 7 if pushed (slight improvement..)
        if pushed_7 > 0 and '7' in possible_heads:
            idx = possible_heads.index('7')
            return possibles[idx], None

        # play 'A' or '8' first
        if 'A' in possible_heads:
            idx = possible_heads.index('A')
            return possibles[idx], None
        if '8' in possible_heads:
            idx = possible_heads.index('8')
            return possibles[idx], None

        # keep jacks for last
        if 'J' in possible_heads:
            rest = [h for h in possibles if h[0]!='J']
            if rest!=[]:
                possibles = rest
                possible_heads = [h[:-1] for h in possibles]

        # keep sevens for last (before jacks)
        if '7' in possible_heads:
            rest = [h for h in possibles if h[0]!='J']
            if rest!=[]:
                possibles = rest

        played = choice(possibles)

        if played[0]=='J':
            choices = [h[-1] for h in hand
                             if h[:-1]!='J']
            if choices == []:
                wanted_suite = played[-1]
            else:
                wanted_suite = choice(choices)

        else:
            wanted_suite = None

        return played, wanted_suite
