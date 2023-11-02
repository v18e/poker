import random
import Card

class Deck():
    def __init__(self):
        self.suit = ["♥","♦","♣","♠"]
        self.value = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
        self.shuffled = []
        self.shuffle()
 
    def shuffle(self):
        kolejnosc = [i for i in range(0, 52)]
        random.shuffle(kolejnosc)
        for i in kolejnosc:
            card = Card(self.suit[i//13], self.value[i%13])       # 0-12 hearts, 13-25 diamonds, 26-38 clubs, 39-51 spades
            self.shuffled.append(card)
    
    def show_shuffled(self): 
        for card in self.shuffled:
            print(card)    

    def get_card(self):
        if not self.shuffled:
            return None 
        return self.shuffled.pop()