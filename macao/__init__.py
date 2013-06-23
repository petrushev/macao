# -*- coding: utf-8 -*-
from random import shuffle
from itertools import groupby
from collections import deque

SUITES = tuple(u'♣♠♦♥')
HEADS = tuple(h for h in map(str, range(2, 11)) + list('JQKA'))
DECK = frozenset(h+s for h in HEADS for s in SUITES)

HAND_SIZE = 6

def new_deck():
    deck = list(DECK)
    shuffle(deck)
    return deque(deck)

def can_play(card, ground):
    """True if `card` can be played on top of `ground`"""
    return card[0] == 'J' or card[:-1] == ground[:-1] or card[-1] == ground[-1]


class Player(object):

    def __init__(self, game, method):
        self.game = game            # game instance (owner)
        self.hand = []              # current hand
        self.has_drawn = False      # did it draw extra already
        self.method = method(self)  # playing strategy (ai)
        self._idx = None

    @property
    def idx(self):
        if self._idx is None:
            self._idx = self.game.players.index(self)
        return self._idx

    def __repr__(self):
        idx = self.idx + 1
        return ('<Player %d: ' % idx ) + ' '.join(self.hand).encode('utf-8')+'>'

    def has_choice(self):
        ground = self.game.ground
        for c in self.hand:
            if can_play(c, ground):
                return True
        return False

    def play(self):
        if not self.has_choice():
            return None, None

        return self.method.play() # play card or play none

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
        self.num_players = len(methods)

        self.pushed_7 = 0 # queue for pushed cards with 7s

        self.winner = None


    def do_turn(self):
        current_player = self.players[self.turn]
        played, wanted_suite = current_player.play()

        if played is None:
            self.handle_skip()
            return

        if played not in current_player.hand:
            print 'Ilegal move'
            return

        played_head = played[:-1]


        if played_head!='J' and played_head!=self.ground[:-1] and played[-1]!=self.ground[-1]:
            print 'Ilegal move'
            return

        print '- %d - :' % (current_player.idx + 1), played.encode('utf-8')

        current_player.hand.remove(played)

        if self.pushed_7 and played_head!='7':
            self.push_7(current_player)

        if len(current_player.hand)==1:
            print '    - %d - :' % (current_player.idx + 1), ' last'

        elif len(current_player.hand)==0:
            print ' WINNER:', (current_player.idx + 1)
            self.winner = current_player
            return

        if played_head=='7':
            self.pushed_7 = self.pushed_7 + 2
            print '    pushed 7:', self.pushed_7

        if played_head in ('A', '8'):
            self.turn = (self.turn + 1) % self.num_players
            print '    < %d > jumped' % (self.turn + 1)

        if played_head=='J':
            print '    changed suite:', wanted_suite.encode('utf-8')
            self.deck.append(played)
            self.ground = 'x' + wanted_suite

        else:
            if self.ground[0]!='x':
                self.deck.append(self.ground)
            self.ground = played

        self.turn = (self.turn + 1) % self.num_players
        current_player.has_drawn = False


    def handle_skip(self):
        current_player = self.players[self.turn]
        print '    < %d >' %  (current_player.idx + 1),

        if self.pushed_7:
            self.push_7(current_player)

        elif current_player.has_drawn is False:
            current_player.hand.append(self.deck.popleft())
            current_player.has_drawn = True
            print '    draw'

        else:
            current_player.has_drawn = False
            self.turn = (self.turn + 1) % self.num_players
            print '    skip'

    def push_7(self, player):
        for _ in range(self.pushed_7):
            player.hand.append(self.deck.popleft())
        print '    gathered 7:', self.pushed_7
        self.pushed_7 = 0
