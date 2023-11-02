class HandEvaluator():              #maybe be checking if pair exist first i can already tell that some doesnt exist 
    def __init__(self, cards):      #return [hand, value, kicker1, kicker2, kicker3, kicker4]  hand: 0 - high card, 1 - pair, 2 - 2pairs...
        self.cards = cards
        self.ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        self.best_hand = None
        self.best_hand_name = None
        self.check_hand()

    def check_hand(self) -> None:   #return nothing 
        ranks_reversed = {value: key for key, value in self.ranks.items()}
        hand = self.check_royal_flush()
        if hand:
            self.best_hand = hand 
            self.best_hand_name = f"Royal flush"
            return 

        hand = self.check_straight_flush()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"Straight flush of high {ranks_reversed[hand[1]]}"
            return

        hand = self.check_quads()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"Four of a kind, {ranks_reversed[hand[1]]}"
            return

        hand = self.check_full_house()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"Full house, three of {ranks_reversed[hand[1]]}, two of {ranks_reversed[hand[2]]}"
            return

        hand = self.check_flush()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"{ranks_reversed[hand[1]]} high flush"
            return

        hand = self.check_straight()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"Straight of high {ranks_reversed[hand[1]]}"
            return

        hand = self.check_three()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"Three of a kind, {ranks_reversed[hand[1]]}"
            return

        hand = self.check_2pairs()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"Two pair, {ranks_reversed[hand[1]]} and {ranks_reversed[hand[2]]}"
            return
        
        hand =  self.check_pair()
        if hand:
            self.best_hand = hand 
            self.best_hand_name = f"One pair, {ranks_reversed[hand[1]]}"
            return

        hand = self.check_high_card()
        if hand:
            self.best_hand = hand
            self.best_hand_name = f"High card, {ranks_reversed[hand[1]]}"
            return

    def check_high_card(self):      #return [1, max_value, kicker1, kicker2, kicker3, kicker4, kicker5]
        values = [self.ranks[card.value] for card in self.cards]
        sorted_values = sorted(values, reverse = True)
        return [1] + sorted_values[:5]
    
    def check_pair(self):           #return [2, pair_value, kicker1, kicker2, kicker3, 0]
        pairs = []
        values = []
        for card in self.cards:
            card_value = self.ranks[card.value]
            if card_value not in values:
                values.append(card_value)
            elif card.value not in pairs:
                pairs.append(card_value)
            else:
                return None
        if len(pairs) != 1:
            return None 
        values.remove(pairs[0])
        values = sorted(values, reverse = True)
        return [2, pairs[0]] + values[:3] + [0] * (4 - len(values[:3]))
    
    def check_2pairs(self):         #return [3, max_pair, second_pair, kicker1, 0, 0]
        pairs = []
        values = []
        for card in self.cards:
            card_value = self.ranks[card.value]
            if card_value not in values:
                values.append(card_value)
            elif card_value not in pairs:
                pairs.append(card_value)
            else:
                return None
        if len(pairs) < 2:
            return None
        sorted_pairs = sorted(pairs, reverse = True)
        values.remove(sorted_pairs[0])
        values.remove(sorted_pairs[1])
        values = sorted(values, reverse = True)
        return [3, sorted_pairs[0], sorted_pairs[1]] + values[:1] + [0] * (3-len(values[:1]))

    def check_three(self):          #return [4, three_value, kicker1, kicker2, 0, 0]
        threes = []
        pairs = []
        values = []
        for card in self.cards:
            card_value = self.ranks[card.value]
            if card_value not in values:
                values.append(card_value)
            elif card.value not in pairs:
                pairs.append(card_value)
            elif card.value not in threes:
                threes.append(card_value)
            else:
                return False
        if len(threes) != 1 or len(pairs) != 1:
            return None
        values.remove(threes[0])
        values = sorted(values, reverse = True)
        return [4, threes[0], values[0], values[1], 0, 0]
    
    def check_straight(self):       #return [5, max_straight_card, 0, 0, 0, 0]
        values = []
        if len(self.cards) < 5:
            return None
        for card in self.cards:
            card_value = self.ranks[card.value]
            values.append(card_value)
        count = 1
        max_straight_value = values[0]
        for i in range(1,len(values)):
            if values[i] == values[i-1] - 1:
                count +=1
                if count == 5:
                    return [6, max_straight_value, 0, 0, 0, 0]
                if count == 4 and values[i] == 2 and values[0] == 14:
                    return [6, 5, 0, 0, 0, 0]
            else:
                if len(values) - i < 5:
                    return None
                max_straight_value = values[i]
                count = 1

    def check_flush(self):          #return [6, max_flush_card, 0, 0, 0, 0]  WARNING! second and nexts cards matters, need to change
        if len(self.cards) < 5:
            return None
        suits = [card.suit for card in self.cards]
        for suit in set(suits):
            if suits.count(suit) >= 5:
                suit_values = [self.ranks[card.value] for card in self.cards if suit == card.suit]
                suit_values_sorted = sorted(suit_values,  reverse = True)
                return [6, suit_values_sorted[0], 0, 0, 0, 0]  
        return None                 

    def check_full_house(self):     #return [7, three_value, pair_value, 0, 0, 0] 
        if len(self.cards) < 5:
            return None
        threes = []
        pairs = []
        values = []
        for card in self.cards:
            card_value = self.ranks[card.value]
            if card_value not in values:
                values.append(card_value)
            elif card_value not in pairs:
                pairs.append(card_value)
            elif card_value not in threes:
                threes.append(card_value)
            else:
                return False
        if len(threes) < 1 or len(pairs) < 2:
            return None
        sorted_threes = sorted(threes, reverse = True)
        pairs.remove(sorted_threes[0])
        sorted_pairs = sorted(pairs, reverse = True)
        return [7, sorted_threes[0], sorted_pairs[0], 0, 0, 0]                    

    def check_quads(self):          #return [8, quad_value, 0, 0, 0, 0]
        values  = [self.ranks[card.value] for card in self.cards]
        for value in set(values):
            if values.count(value) == 4:
                return [8, values, 0, 0, 0, 0]
        return None

    def check_straight_flush(self): #return [9, max_straight_card, 0, 0, 0, 0]
        if len(self.cards) < 5:
            return None
        suits = [card.suit for card in self.cards]
        for suit in set(suits):
            if suits.count(suit) >= 5:
                suit_values = [self.ranks[card.value] for card in self.cards if suit == card.suit]
                suit_values_sorted = sorted(suit_values,  reverse = True)
                max_straight_value = suit_values_sorted[0]
                count = 1
                for i in range(1,len(suit_values_sorted)):
                    if suit_values_sorted[i] == suit_values_sorted[i-1] - 1:
                        count += 1
                        if count == 5:
                            return [9, max_straight_value, 0, 0, 0, 0]
                        if count == 4 and suit_values_sorted[i] == 2 and suit_values_sorted[0] == 14:
                            return [9, 5, 0, 0, 0, 0]
                    else:
                        if len(suit_values_sorted) - i < 5:
                            return None
                        max_straight_value = suit_values_sorted[i]
                        count = 1

    def check_royal_flush(self):    #return [10, 14, 0, 0, 0, 0]
        flush = self.check_straight_flush()
        if flush and flush[1] == 14:
            return [10, 14, 0, 0, 0, 0] 
        else:
            return None    
