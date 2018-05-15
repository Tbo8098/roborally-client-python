from itemDescription import *
from random import *


listOfPlayers = []
cardNumbersUsed = [] 

class users():
    def __init__(self, name):
        self.name = name
        self.cards = []

    def deckOfCards(self):
        while len(self.cards) < 9:

            card_number = randint(100,399)

            if card_number is not cardNumbersUsed:

                if card_number > 100 and card_number < 150:
                    card_class = cards[100]
                elif card_number > 150 and card_number < 200:
                    card_class = cards[150]
                elif card_number > 200 and card_number < 250:
                    card_class = cards[200]
                elif card_number > 250 and card_number < 300:
                    card_class = cards[250]
                elif card_number > 300 and card_number < 350:
                    card_class = cards[300]
                elif card_number > 350 and card_number < 400:
                    card_class = cards[350]

                self.cards.append([card_class, card_number])
                cardNumbersUsed.append(card_number)

    
    def print_it_out(self):
        print(self.name)
        print(self.cards)

        

listOfPlayers.append(users('tyler'))
listOfPlayers.append(users('curtis'))


for i in listOfPlayers:
    i.deckOfCards()
    i.print_it_out()

print(sort(cardNumbersUsed))







    