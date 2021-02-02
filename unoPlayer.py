from cardMethods import hand

class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []

    def botPlay(self, top):
        suit = top[0]
        number = top[1:]
        Hand = []
        for x in self.hand:
            Hand.append([x[0], x[1:]])
        suits = 0
        numbers = 0
        wilds = 0
        for x in Hand:
            if x[0] == suit:
                suits += 1
            if x[1] == number:
                numbers += 1
            if x[0] == 'W':
                wilds += 1
        if not suits and not numbers and not wilds:
            return False
        elif not suits and not numbers and wilds:
            play = 'W'
        elif numbers > suits:
            play = 'n'
        else:
            play = 's'
        if play == 'n':
            R = 0
            Y = 0
            B = 0
            G = 0
            for x in Hand:
                if x[1] == number and x[0] == 'R':
                    R += 1
                if x[1] == number and x[0] == 'Y':
                    Y += 1
                if x[1] == number and x[0] == 'B':
                    B += 1
                if x[1] == number and x[0] == 'G':
                    G += 1
            lst = sorted([R, Y, B, G])
            if lst[-1] == R:
                play = 'R'
            if lst[-1] == Y:
                play = 'Y'
            if lst[-1] == B:
                play = 'B'
            if lst[-1] == G:
                play = 'G'
            play = play + number
        if play == 's':
            lst = []
            for x in Hand:
                if x[0] == suit:
                    lst.append(x[1])
            lst = sorted(lst)
            play = lst[-1]
            play = suit + play
        if play == 'W':
            if 'W-4' in self.hand:
                play = 'W-4'
            else:
                play = 'W-1'
        self.hand.remove(play)
        return play

    def realPlay(self, topCard, deck):
        Hand = hand(self.hand, deck)
        print('Your hand: ', ', '.join(Hand))
        check = True
        while check:
            choice = -1
            while int(choice) not in range(0, len(self.hand) + 1):
                    choice = input('Enter corresponding number for card you would like to play, or 0 for draw: ')
                    if choice == '':
                        choice = -1
            if int(choice) == 0:
                print()
                return False
            else:
                card = -1
                for x in Hand:
                    if x[0] == choice:
                        card = Hand.index(x)
            card = self.hand[card]
            if card[0] != topCard[0] and card[1:] != topCard[1:] and card != 'W-1':
                print('Card does not match color or number.')
                continue
            else:
                self.hand.remove(card)
                print()
                return card

    def realWild(self):
        choice = 0
        while choice not in [1,2,3,4]:
            choice = int(input('Enter 1 for Green, 2 for Yellow, 3 for Blue, or 4 for Red: '))
        colors = ['G-1', 'Y-1', 'B-1', 'R-1']
        return colors[choice - 1]

    def botWild(self, Hand):
        R = 0
        Y = 0
        B = 0
        G = 0
        for x in Hand:
            if x[0] == 'R':
                R += 1
            if x[0] == 'Y':
                Y += 1
            if x[0] == 'B':
                B += 1
            if x[0] == 'G':
                G += 1
        lst = sorted([R, Y, B, G])
        if lst[-1] == R:
            play = 'R-1'
        if lst[-1] == Y:
            play = 'Y-1'
        if lst[-1] == B:
            play = 'B-1'
        if lst[-1] == G:
            play = 'G-1'
        return play
