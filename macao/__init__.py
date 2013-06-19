# -*- coding: utf-8 -*-
from random import shuffle
from itertools import groupby
from collections import deque

SUITES = tuple(u'♣♠♦♥')
HEADS = tuple(h for h in map(str, range(2, 11)) + list('JQKA'))
DECK = frozenset(h+s for h in HEADS for s in SUITES)

HAND_SIZE = 4

def new_deck():
    deck = list(DECK)
    shuffle(deck)
    return deque(deck)


def can_play(card, ground):
    """True if `card` can be played on top of `ground`"""
    return (card[:-1] == ground[:-1]) or (card[-1] == ground[-1])


class Player(object):

    def __init__(self, game, method):
        self.game = game            # game instance (owner)
        self.hand = []              # current hand
        self.has_drawn = False      # did it draw extra already
        self.method = method(self)  # playing strategy (ai)

    def __repr__(self):
        idx = self.game.players.index(self) + 1
        return ('<Player %d: ' % idx ) + ' '.join(self.hand).encode('utf-8')+'>'

    def play(self):
        #TODO: move 'win' mechanics to Game class
        # if empty hand - announce win
        if len(self.hand)==0:
            self.game.won(self)
        else:
            self.method.play()

    def play_card(self, played):
        self.has_drawn = False
        self.hand.remove(played)  # remove played card from hand
        self.game.turned(played)  # notify game (callback)

    def draw(self):
        if self.has_drawn:
            # draws second time
            self.has_drawn = False
            self.game.turned(None)  # notify empty

        else:
            # draws first time
            self.has_drawn = True
            self.hand.append(self.game.deal_extra())  # update hand
            self.method.play()  # goto play after update


class Game(object):

    def __init__(self, methods):
        self.deck = new_deck()
        self.players = []

        for method in methods:
            # init player
            p = Player(game = self, method = method)
            for _ in range(HAND_SIZE):
                p.hand.append(self.deck.popleft())
            self.players.append(p)

        self.ground = self.deck.popleft()
        self.turn = 0   # which player's current turn is it
        self.finished = False
        self.num_players = len(methods)

    def do_turn(self):
        self.players[self.turn].play()

    def deal_extra(self):
        print '- %d -   fetched extra' % (self.turn + 1)
        return self.deck.popleft()

    def turned(self, played):
        current = self.turn + 1
        if played is not None:
            self.deck.append(self.ground)  # put current ground back in deck
            self.ground = played   # update ground

            print '- %d -  ' % current, played

            p = self.players[self.turn]

            # announce last
            if len(p.hand)==1:
                print '- %d -   ultimate' % current

            # check for jumps
            head = played[:-1]
            if head in ('A','8'):
                self.turn = (self.turn + 1) % self.num_players
                print '- %d -   jumped' % (self.turn + 1)

        else:
            print '- %d -   skip' % current

        self.turn = (self.turn + 1) % self.num_players

    def won(self, player):
        self.announce_win(player)

    def announce_win(self, player):
        print 'won player' , player
        self.finished = True
        for p_id, p in enumerate(self.players):
            if p == player: continue
            print p
        print 'remaining in deck:', len(self.deck)
