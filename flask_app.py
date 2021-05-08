from flask import Flask, request, session
from cardMethods import deckBuilder, hand
from random import shuffle

app = Flask(__name__)
app.config["DEBUG"] = False
app.config["SECRET_KEY"] = "alkjsklawugh"


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
        session['output'] += 'Your hand: ', ', '.join(Hand) + '\n'
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
        elif lst[-1] == Y:
            play = 'Y-1'
        elif lst[-1] == B:
            play = 'B-1'
        else:
            play = 'G-1'
        return play


def rebuild(topCard=''):
    draw, deck = deckBuilder(2, joker='Zero', jokerOption=1, option=1, ten='Wild', eleven='Skip', twelve='Reverse', thirteen='Draw Two',
                                  ace='One', suit1='Red', suit2='Yellow', suit3='Blue', suit4='Green')

    i = 1
    for x in draw:
        if x[1:] == '10':
            if i % 2 == 0:
                draw[draw.index(x)] = 'W-1'
            else:
                draw[draw.index(x)] = 'W-4'
            i += 1

    deck['G-1'] = 'Green Wild'
    deck['B-1'] = 'Blue Wild'
    deck['Y-1'] = 'Yellow Wild'
    deck['R-1'] = 'Red Wild'
    deck['G-4'] = 'Green Wild Draw 4'
    deck['B-4'] = 'Blue Wild Draw 4'
    deck['Y-4'] = 'Yellow Wild Draw 4'
    deck['R-4'] = 'Red Wild Draw 4'
    deck['W-1'] = 'Wild'
    deck['W-4'] = 'Wild Draw 4'

    for x in session["players"]:
        for y in x.hand:
            draw.remove(y)
    if topCard != '':
        draw.remove(topCard)
        discard = [topCard]
    else:
        discard = [draw[0]]
        draw.pop(0)
    return deck, draw, discard


@app.route("/", methods=["GET", "POST"])
def uno_play():
    if "draw" not in session:
        session["draw"] = []
    if "deck" not in session:
        session["deck"] = []
    if "discard" not in session:
        session["discard"] = []
    if "game" not in session:
        session["game"] = 0
    if "GAME" not in session:
        session["GAME"] = False
    if "outputs" not in session:
        session["outputs"] = ""

    if request.method == "GET":
        draw, deck = deckBuilder(2, joker='Zero', jokerOption=1, option=1, ten='Wild', eleven='Skip', twelve='Reverse', thirteen='Draw Two',
                                  ace='One', suit1='Red', suit2='Yellow', suit3='Blue', suit4='Green')

        i = 1
        for x in draw:
            if x[1:] == '10':
                if i % 2 == 0:
                    draw[draw.index(x)] = 'W-1'
                else:
                    draw[draw.index(x)] = 'W-4'
                i += 1

        deck['G-1'] = 'Green Wild'
        deck['B-1'] = 'Blue Wild'
        deck['Y-1'] = 'Yellow Wild'
        deck['R-1'] = 'Red Wild'
        deck['G-4'] = 'Green Wild Draw 4'
        deck['B-4'] = 'Blue Wild Draw 4'
        deck['Y-4'] = 'Yellow Wild Draw 4'
        deck['R-4'] = 'Red Wild Draw 4'
        deck['W-1'] = 'Wild'
        deck['W-4'] = 'Wild Draw 4'

        discard = [draw[0]]
        draw.pop(0)
        session["draw"] = draw
        session['deck'] = deck
        session['discard'] = discard


        return '''
            <html>
                <body>
                    <p>Enter your name:</p>
                    <form method="post" action=".">
                        <p><input name="name" /></p>
                        <p><input type="submit" name="action" value="Confirm Name" /></p>
                    </form>
                </body>
            </html>
        '''

    if session["game"] == 0:
        player = Player(request.form['name'])
        bot1 = Player('Melody')
        bot2 = Player('Pumpkin')
        bot3 = Player('Athena')

        if "scores" not in session:
            session["scores"] = {bot1.name: 0, bot2.name: 0, bot3.name: 0, player.name: 0}
        if "players" not in session:
            session["players"] = [player, bot1, bot2, bot3]
        session["GAME"] = True

    while session["GAME"]:

        if session['game'] == 0:
            shuffle(session["players"])
            for x in range(5):
                for y in session["players"]:
                    y.hand.append(session["draw"][0])
                    session["draw"].pop(0)
            session["outputs"] += 'Starting card: ', session["deck"][session["discard"][-1]], "\n\n"
            session["game"] = 1
            session['outputs'] += "Round 1\n\n"

        effect = True
        play = True
        while play:
            for x in session["players"]:
                if len(session["draw"]) < 3:
                    session["deck"], session["draw"], session["discard"] = rebuild(session["discard"][-1])
                if session["discard"][-1][1:] == '11' and not effect:
                    session['outputs'] += x.name + "'s turn is skipped.\n"
                    effect = True
                    continue
                if session["discard"][-1][1:] == '13' and not effect:
                    session['output'] += x.name + ' drew two cards.\n'
                    x.hand.append(session["draw"][0])
                    x.hand.append(session["draw"][1])
                    session["draw"].pop(0)
                    session["draw"].pop(0)
                    effect = True
                    continue
                if session["discard"][-1][1:] == '-4' and not effect:
                    session['outputs'] += x.name + ' drew four cards.\n'
                    for i in range(4):
                        x.hand.append(session["draw"][0])
                        session["draw"].pop(0)
                    effect = True
                    continue
                if x == player:
                    session['outputs'] += bot1.name + ' has ' + str(len(bot1.hand)) + ' card[s], ' + bot2.name + ' has ' + \
                                          str(len(bot2.hand)) + ' card[s], ' +bot3.name + ' has ' + str(len(bot3.hand)) + ' card[s]\n'
                    session['outputs'] += f'\nTop card: {session["deck"][session["discard"][-1]]}\n'
                    session["players"] = [session["players"][session["players"].index(x)], session["players"][session["players"].index(x) - 3], session["players"][session["players"].index(x) - 2],
                               session["players"][session["players"].index(x) - 2]]
                    return x.realPlay(session["discard"][-1], session["deck"])
                else:
                    check = x.botPlay(session["discard"][-1])
                    if check == 'W-1' or check == 'W-4':
                        check = x.botWild(x.hand)
                if not check:
                    x.hand.append(session["draw"][0])
                    session['outputs'] += x.name + ' drew.\n'
                    session["draw"].pop(0)
                else:
                    session['outputs'] += x.name + ' played ' + session["deck"][check] + '\n'
                    session["discard"].append(check)
                    effect = False
                if len(x.hand) == 0:
                    session['outputs'] += x.name + ' wins this round!\n'
                    play = False
                    break
                if session["discard"][-1][1:] == '12' and not effect:
                    session["players"] = [session["players"][session["players"].index(x) - 1], session["players"][session["players"].index(x) - 2],
                               session["players"][session["players"].index(x) - 3], session["players"][session["players"].index(x)]]
                    effect = True
                    break


