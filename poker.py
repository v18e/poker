import random 
from HandEvaluator import HandEvaluator
from Card import Card
from Deck import Deck
from Player import Player

class Game():
    def __init__(self, players, big_blind = 20, small_blind = 10):
        self.players = players #0= SB #1= BB
        self.dealer_cards = []
        self.deck = Deck()
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.max_active_bet = big_blind
        self.active_players = players
        self.pot = small_blind + big_blind
        self.minimal_bet = big_blind 

    def deal_players_cards(self):
        for player in self.players:
            player.draw_cards(self.deck)
            
    def dealer_draw(self, number=5):
        if not self.deck.shuffled:
            raise ValueError("Deck not avaliable")
        for _ in range(number):
            card = self.deck.get_card()
            if card:
                self.dealer_cards.append(card)
            else:
                return False
        return True

    def show_flop(self):
        print(*self.dealer_cards[:3])   
    
    def show_turn(self):    
        print(*self.dealer_cards[:4])

    def show_river(self):
        print( *self.dealer_cards[:5])

    def bet_input(self, player, possible_moves):   #reutrn [a, b]   a = decision(1-fold, 2-check, 3-call, 4-bet) b = amount of bet
        while True:
            try: 
                if 3 in possible_moves:
                    decision = int(input(f"{player.nick} input your decision: 1 for Fold, 3 for Call, 4 for Bet, your balance is {player.balance}: "))  
                elif 2 in possible_moves:
                    decision = int(input(f"{player.nick} input your decision: 1 for Fold, 2 for Check, 4 for Bet, your balance is {player.balance}: "))
                    

                if decision == 1:
                        return [1,0]
                elif decision == 2:  
                    if 2 in possible_moves:   
                        return [2,0]
                    else:
                        print("You cant check, you have to fold, call or bet")
                elif decision == 3:
                    if 3 in possible_moves:
                        return [3,min(player.balance, self.max_active_bet)]
                    else:
                        print("You cant call, you have to fold, check or bet")
                elif decision == 4:
                    while True:
                        try:
                            bet = input(f"{player.nick} place your bet, type 'b' to go back: ")
                            if str(bet) == 'b':
                                break
                            bet = int(bet)
                            if player.balance >= bet >= max(2*self.max_active_bet, self.minimal_bet):
                                return [4,bet]
                            elif bet > player.balance:  #allin situation
                                return [4,player.balance]   
                            elif max(2*self.max_active_bet, self.minimal_bet) > bet: 
                                print(f"You must bet at least {max(2*self.max_active_bet, self.minimal_bet)}, go allin or fold")  #ELSE??
                        except ValueError:
                            print(f"Invalid input, please enter number between minimal bet - {self.max_active_bet} and your balance - {player.balance}" ) #write what is minimal bet and balance
            except ValueError:
                if 2 in possible_moves:
                    print("Invalid input, please enetr number 1, 2, 3 or 4")
                else:  
                    print("Invalid input, please enetr number 1, 3 or 4")
    
    def play_betting(self, active_even_bet_count = 0, start = False):
        
        if start:  #start guy +1 from BB
            current_player_index = 2%len(self.active_players)
        else:  #start from nearest to SB 
            current_player_index = 0 
        while len(self.active_players) > 1 and active_even_bet_count < len(self.active_players):
            player = self.active_players[current_player_index]
            if self.max_active_bet == 0:
                decision, bet = self.bet_input(player, possible_moves=[1,2,4])
            else:
                decision, bet = self.bet_input(player, possible_moves=[1,3,4])
            if decision == 1:
                player.fold()
                self.active_players.remove(player)
            elif decision == 2:
                player.check()
                active_even_bet_count += 1
            elif decision == 3:
                self.pot += bet - player.get_player_bet()
                active_even_bet_count += 1
                player.call(bet)
            else:
                self.pot += bet - player.get_player_bet()
                player.place_bet(bet)
                self.max_active_bet = bet
                active_even_bet_count = 1
            current_player_index = (current_player_index + 1) % len(self.active_players)
        
        if len(self.active_players) == 1:
            self.active_players[0].receive_winnings(self.pot)
            print(f"{self.active_players[0].nick} has won {self.pot} pot")
            return True
        
        self.max_active_bet = 0
        return False
    
    def play_community_cards(self, cards, number):
        for player in self.active_players:
            player.extend_with_dealer_cards(cards)
            hand_ev = HandEvaluator(player.cards)
            print(f"{player.nick} has {player.show_players_cards(number)} - {hand_ev.best_hand_name} with balance: {player.balance} ")

    def winner(self):                   #didnt test if it works, also dont have exception when there is all in and pot should be split to some players except all in in some range
        def concatenate_and_compare(hand1, hand2):
            hand1_c = (''.join(format(i, '02') for i in hand1))
            hand2_c = (''.join(format(i, '02') for i in hand2))
            if hand1_c == hand2_c:
                return "draw"
            elif hand1_c > hand2_c:   #bez sensu to jest w ogole, trzeba odrazu z playerem jakos to powiazac
                return hand1
            else:
                return hand2
        
        winners = []
        best_hand = [0,0,0,0,0,0]
        
        for player in self.active_players:
            player_hand_evaluator = HandEvaluator(player.cards)
            compare = concatenate_and_compare(player_hand_evaluator.best_hand, best_hand)
            if compare == "draw":
                winners.append(player)
            elif compare == player_hand_evaluator.best_hand:
                best_hand = player_hand_evaluator.best_hand
                winners = [player]
        winners_message = ""
        for player in winners:
            player.receive_winnings(self.pot//len(winners))
            winners_message += f"{player.nick} "
        print(winners_message + "has won a hand")

    def set_active_players_deafult(self):
        for player in self.active_players:
            player.set_player_bet_zero()

    def play(self):   #todo:
        self.dealer_draw()
        self.active_players = self.players.copy()
        self.set_active_players_deafult()
        self.players[0].place_bet(self.small_blind)
        self.players[1].place_bet(self.big_blind)
        self.deal_players_cards()
        self.play_community_cards([], number = 2)
        if self.play_betting( active_even_bet_count = 1,start = True):  #if True RETURN, because it means that 1 player remaining 
            return     
        print("Flop: ")
        self.show_flop()
        self.play_community_cards(self.dealer_cards[:3], number = 2)
        self.set_active_players_deafult()
        if self.play_betting():
            return 
        print("Turn: ")
        self.show_turn()
        self.play_community_cards([self.dealer_cards[3]], number = 2 )
        self.set_active_players_deafult()
        if self.play_betting():
            return 
        print("River: ")
        self.show_river()
        self.play_community_cards([self.dealer_cards[4]], number = 2)
        self.set_active_players_deafult()
        if self.play_betting():
            return 
        self.winner()
        for player in self.active_players:
            print(f"{player.nick} has {player.balance}")

p1 = Player("vibe")
p2 = Player("such")
p3 = Player("stah")
players = [p1,p2,p3]
hand = Game(players)
hand.play()

