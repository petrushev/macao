from random import choice, random

from macao import can_play, SUITES

class Strategy(object):
    def __init__(self, player):
        self.player = player

class Human(Strategy):

    def play(self):
        player = self.player
        hand = list(player.hand)
        ground = player.game.ground

        pushed_7 = player.game.pushed_7

        print ' '.join(hand).encode('utf-8'),' | ', ground.encode('utf-8')

        # check if there is no way to play
        possibles = [h for h in hand if can_play(h, ground)]
        if len(possibles)==0:
            if pushed_7 > 0:
                player.gather_7()
                return self.play()

            return self.draw()

        # enter valid card for playing, 0 for draw
        ord_ = '-1'
        while not(ord_.isdigit()) or int(ord_) < 0 or int(ord_) > len(hand):
            ord_ = raw_input()
            ord_ = ord_.strip()
        ord_ = int(ord_)

        # 0 is for drawing card or skipping
        if ord_ == 0:
            if pushed_7 > 0:
                player.gather_7()
                return self.play()

            return self.draw()

        played = hand[ord_-1]
        if not can_play(played, ground):
            print 'invalid game'
            return self.play()

        # pushed cards with 7 but player plays otherwise - got to gather
        if pushed_7 > 0 and played[0]!='7':
            player.gather_7()

        # play the card
        if played[0]=='J':
            # played Jack, need to change suite
            ord_ = '0'
            while not(ord_.isdigit()) or int(ord_) < 1 or int(ord_) > 4:
                ord_ = raw_input(' '.join(tuple(SUITES)).encode('utf-8')+' : ')
                ord_ = ord_.strip()
            ord_ = int(ord_) - 1

            suite = SUITES[ord_]
            player.play_card(played, wanted_suite=suite)

        else:
            player.play_card(played)

    def draw(self):
        self.player.draw()


class RandomAi(Strategy):

    def play(self):
        player = self.player
        hand = list(self.player.hand)
        ground = player.game.ground
        pushed_7 = player.game.pushed_7

        # check if there is no way to play
        possibles = [h for h in hand if can_play(h, ground)]
        if len(possibles)==0:
            if pushed_7 > 0:
                player.gather_7()
                return self.play()

            return self.draw()

        if random() > .7:
            possibles.append(0) # possibly bluff for new card
        played = choice(possibles)

        if played == 0:
            if pushed_7 > 0:
                player.gather_7()
                return self.play()

            return self.draw()

        if pushed_7 > 0 and played[0]!='7':
            player.gather_7()

        if played[0]=='J':
            # laplace smoothed for random suites
            choices = [h[-1] for h in player.hand] + list(SUITES)
            suite = choice(choices)
            player.play_card(played, wanted_suite = suite)

        else:
            player.play_card(played)

    def draw(self):
        self.player.draw()
