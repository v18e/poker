class Player():
    def __init__(self, nick, balance = 1000 ):  
        self.nick = nick
        self.balance = balance 
        self.cards = []
        self.bet = 0

    def fold(self):    # clears player cards, print folds
        print(f"{self.nick} folds ")
        self.cards = []

    def check(self):    # doint nothing, only for print purposes
        print(f"{self.nick} checks ")

    def call(self, amount):
        self.balance -= amount - self.bet
        self.bet = amount
        print(f"{self.nick} calls: {amount} ")

    def place_bet(self, amount): #       what with re reise ??????? 
        self.balance -= amount - self.bet  
        self.bet = amount 
        print(f"{self.nick} bets: {self.bet}")

    
    def receive_winnings(self, winnings):  
        self.balance += winnings

    def draw_cards(self, deck, number=2 ):  #draw cards for player, return True    
        if not deck:
            raise ValueError("No deck avaliable")  #shoud never happend
        for _ in range(number):
            card = deck.get_card()
            if card:
                self.cards.append(card)  
        return True
    
    
    def get_player_bet(self):
        return self.bet
    
    def set_player_bet_zero(self):
        self.bet = 0

    def extend_with_dealer_cards(self, deck): 
        self.cards.extend(deck)

    def clear_player_cards(self):
        self.cards = []
        self.bet = 0 
    
    def show_players_cards(self, number = 2):    # why somewhere there is return and not return and return with print and print without string wtf
        cards_str = ' '.join(str(self.cards[card]) for card in range(number))
        return f"{cards_str}"