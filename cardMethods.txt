import random

def deckBuilder(decks, option=2, joker='', jokerOption=0, ace='Ace', ten='Ten', eleven='Jack', twelve='Queen', thirteen='King', suit1='Spades', suit2='Hearts', suit3='Clubs', suit4=
'Diamonds'):
    deck = {}
    suits = [suit1, suit2, suit3, suit4]
    faces = [ace, 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', ten, eleven, twelve, thirteen]
    for x in suits:
        z = 1
        for y in faces:
            if option == 2:
                deck[x[0] + str(z)] = y + ' of ' + x
            if option == 1:
                deck[x[0] + str(z)] = x + ' ' + y
            z += 1
    pile = list(deck.keys())
    if joker != '' and jokerOption == 0:
        for x in range(2):
            pile.append(joker[0] + '0')
        deck[joker[0] + '0'] = joker
    draw = []
    for x in range(decks):
        draw += pile
    if jokerOption == 1:
        for x in range(int(decks/2)):
            for x in suits:
                pile.append(x[0] + '0')
                deck[x[0] + '0'] = x + ' ' + joker
    random.shuffle(draw)
    return draw, deck

def hand(self, deck):
        x = 1
        hand = []
        for y in self:
            hand.append(f'{x}: {deck[y]}')
            x += 1
        return hand
