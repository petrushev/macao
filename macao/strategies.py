from random import choice, shuffle, random

from macao import can_play

class Strategy(object):
    def __init__(self, player):
        self.player = player

class Human(Strategy):

    def play(self):
        hand = list(self.player.hand)
        ground = self.player.game.ground

        print ' '.join(hand).encode('utf-8'),' | ', ground.encode('utf-8')

        # check if there is no way to play
        possibles = [h for h in hand if can_play(h, ground)]
        if len(possibles)==0:
            return self.draw()

        # enter valid card for playing, 0 for draw
        ord_ = '-1'
        while not(ord_.isdigit()) or int(ord_) < 0 or int(ord_) > len(hand):
            ord_ = raw_input()
            ord_ = ord_.strip()
        ord_ = int(ord_)

        if ord_ == 0:
            return self.draw()

        played = hand[ord_-1]
        can_ = can_play(played, ground)
        if not can_:
            print 'invalid game'
            return self.play()

        # play the card
        self.player.play_card(played)

    def draw(self):
        self.player.draw()

class RandomAi(Strategy):

    def play(self):
        hand = list(self.player.hand)
        ground = self.player.game.ground

        # check if there is no way to play
        possibles = [h for h in hand if can_play(h, ground)]
        if len(possibles)==0:
            return self.draw()

        if random() > .7:
            possibles.append(0) # possibly bluff for new card
        played = choice(possibles)
        if played == 0:
            return self.draw()

        self.player.play_card(played)

    def draw(self):
        self.player.draw()
