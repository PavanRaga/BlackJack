'''
1. Create a deck of 52 cards
2. Shuffle
3. wait for player
4. Read player chips value
5. if value>min bet, provide two cards to player
6. two cards to dealer. Display only one
7. Ask for hit/stay
8. if hit, give one card
9. Check if 21
10. Check if more than 21
11 if stay, hit dealer till he beats the player or goes above 21.
Classes:
1. Dealer
attr: Deck
method:
    Deal
    check21
    winner
    hit
    stay
2. Player
attr: chips
method:
    join
    hit
    stay
    quit
3. Deck
attr: deck
method:
    reset
    shuffle
    pop
'''
import random
from time import sleep
from collections import defaultdict

cards = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

deck = defaultdict(dict)
deck['Hearts'] = cards
deck['Diamonds'] = cards
deck['Spades'] = cards
deck['Clubs'] = cards

class deck_class():
    def __init__(self, init_deck):
        self.deck = dict(init_deck)
    def reset(self):
        global deck
        self.deck = dict(deck)
    def pop(self):
        self.suit, self.cards = random.choice(list(self.deck.items()))
        self.card = random.choice(list(self.cards.items()))
        return (self.suit, self.card)

class player():
    def __init__(self, chips):
        self.chips = chips
        self.cards = ()
    def pay(self,bet):
        if (bet > self.chips):
            return 0
        else:
            self.chips -= bet
            return 1
    def chips_left(self):
        return self.chips
    def cardss(self,*card0):
        #print(self.cards)
        self.cards = self.cards + card0
        #print(self.cards)
    def get_cards(self):
        return self.cards
    def get_card_value(self):
        #print(self.cards)
        values = [value[1][1] for value in self.cards]
        #print(values)
        return sum(values)

class dealer():
    def __init__(self,player):
        self.player = player
        global deck
        self.deck = deck_class(deck)
        self.cards = ()
    def deal(self):
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        card3 = self.deck.pop()
        card4 = self.deck.pop()
        return (card1,card2,card3,card4)
    def check21(self,cards):
        if cards == 21:
            self.winner('\t player',cards)
            return 1
        elif cards > 21:
            self.lose('\t player',cards)
            return 1
        else:
            return 0
    def winner(self,player,value):
        print("{} wins with card value: {}!".format(player, value))
    def lose(self,player,value):
        print("{} loses with card value: {}!".format(player, value))
    def hit(self):
        return (self.deck.pop())
    def cardss(self,*card0):
        self.cards = self.cards + card0
        #print(self.cards)
        #print(card0)
    def get_cards(self):
        return self.cards
    def get_card_value(self):
        values = [value[1][1] for value in self.cards]
        return sum(values)
    def reset(self):
        self.deck.reset()

play = 1
min_bet = 10
win = False

print("Welcome to BlackJack!")

while(play):
    player1 = player(100)
    dealerman = dealer(player1)
    game_over = 0
    print("Please bet {} to proceed".format(min_bet))
    bet = int(input())
    if bet < min_bet:
        print("Bet isn't enough to proceed")
        continue
    if not player1.pay(bet):
        print("Looks like you dont have enough chips to play!")
        continue
    print("Dealing..", end="")
    sleep(0.5)
    print("..")
    card = dealerman.deal()
    #print(card)
    dealerman.cardss(card[0],card[1])
    player1.cardss(card[2],card[3])
    print("Dealer's one card value: {}".format(card[0][1][1]))
    if dealerman.check21(player1.get_card_value()):
        pass
    else:
        hit = 1
        while(hit):
            print("Player's card value: {}".format(player1.get_card_value()))
            print("Do you want to hit?(1/0)")
            hit = int(input())
            if not hit:
                continue
            else:
                player1.cardss(dealerman.hit())
                if dealerman.check21(player1.get_card_value()):
                    game_over=1
                    break
                else:
                    continue
        #player1 done, dealer
        # print(game_over)
        # means player chose to stop the hit before game over
        if not game_over:
            while(dealerman.get_card_value() < 21):
                dealerman.cardss(dealerman.hit())
                print("Dealer's card value after hit {}".format(dealerman.get_card_value()))
                if (dealerman.get_card_value() <= 21 and dealerman.get_card_value() > player1.get_card_value()):
                    dealerman.winner('\t Dealer', dealerman.get_card_value())
                    win = True
            if not win:
                dealerman.winner('\t player1', player1.get_card_value())
