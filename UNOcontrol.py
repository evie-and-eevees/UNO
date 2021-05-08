from random import shuffle
from unoPlayer import Player
import cardMethods as meth


bot1 = Player('Melody')
bot2 = Player('Pumpkin')
bot3 = Player('Athena')
name = input('Enter your name: ')
player = Player(name)
    
scores = {bot1.name: 0, bot2.name: 0, bot3.name: 0, player.name: 0}
players = [player, bot1, bot2, bot3]
    
def rebuild(topCard=''):
    draw, deck = meth.deckBuilder(2, joker='Zero', jokerOption=1, option=1, ten='Wild', eleven='Skip', twelve='Reverse', thirteen='Draw Two',
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

    for x in players:
        for y in x.hand:
            draw.remove(y)
    if topCard != '':
        draw.remove(topCard)
        discard = [topCard]
    else:
        discard = [draw[0]]
        draw.pop(0)
    return deck, draw, discard
    
game = 1
GAME = True
while GAME:
        shuffle(players)
        print('Round: ', game)
        deck, draw, discard = rebuild()
        for x in range(5):
            for y in players:
                y.hand.append(draw[0])
                draw.pop(0)
        print('Starting card: ', deck[discard[-1]])
        print()
    
        effect = True
        play = True
        while play:
            for x in players:
                if len(draw) < 3:
                    deck, draw, discard = rebuild(discard[-1])
                if discard[-1][1:] == '11' and not effect:
                    print(x.name + "'s turn is skipped.")
                    effect = True
                    continue
                if discard[-1][1:] == '13' and not effect:
                    print(x.name + ' drew two cards.')
                    x.hand.append(draw[0])
                    x.hand.append(draw[1])
                    draw.pop(0)
                    draw.pop(0)
                    effect = True
                    continue
                if discard[-1][1:] == '-4' and not effect:
                    print(x.name + ' drew four cards.')
                    for i in range(4):
                        x.hand.append(draw[0])
                        draw.pop(0)
                    effect = True
                    continue
                if x == player:
                    print()
                    print(bot1.name + ' has ' + str(len(bot1.hand)) + ' card[s], ' + bot2.name + ' has ' +
                          str(len(bot2.hand)) + ' card[s], ' +bot3.name + ' has ' + str(len(bot3.hand)) + ' card[s]')
                    print(f'\nTop card: {deck[discard[-1]]}')
                    check = x.realPlay(discard[-1], deck)
                    if check == 'W-1' or check == 'W-4':
                        check = x.realWild()
                else:
                    check = x.botPlay(discard[-1])
                    if check == 'W-1' or check == 'W-4':
                        check = x.botWild(x.hand)
                if not check:
                    x.hand.append(draw[0])
                    print(x.name + ' drew.')
                    draw.pop(0)
                else:
                    print(x.name + ' played ' + deck[check])
                    discard.append(check)
                    effect = False
                if len(x.hand) == 0:
                    print(x.name + ' wins this round!')
                    play = False
                    break
                if discard[-1][1:] == '12' and not effect:
                    players = [players[players.index(x) - 1], players[players.index(x) - 2],
                               players[players.index(x) - 3], players[players.index(x)]]
                    effect = True
                    break
        game += 1
        for y in players:
            for x in y.hand:
                if int(x[1:]) > 10:
                    y.hand[y.hand.index(x)] = x[0] + '20'
                if int(x[1:]) < 0:
                    y.hand[y.hand.index(x)] = x[0] + '50'
            scores[y.name] += sum(int(x[1:]) for x in y.hand)
            y.hand.clear()
        print('Score: ', scores)
        for x in scores.values():
            if x >= 150:
                GAME = False
        if GAME:
            input('Press enter when ready for next round.')
        else:
            input('Game over! Press enter to see final scores.')
        print()
winner = ['', 150]
for x in scores:
    if scores[x] < winner[1]:
        winner = [x, scores[x]]
    print('The winner is: ', winner, '!!!!')
