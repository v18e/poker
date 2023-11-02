import random 
import HandEvaluator
import Deck 
import Player



 

class Game():
    def __init__(self, players, big_blind = 20, small_blind = 10):
        self.players = players
        self.dealer_cards = []
        self.deck = Deck()
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.minimal_bet = big_blind
        self.active_players = players
        self.pot = small_blind + big_blind  

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

    def bet_input(self, player):
        while True:
            try:
                decision = int(input(f"{player.nick} input your decision: 1 for Fold, 2 for Check, 3 for Bet, your balance is {player.balance}: "))
                if decision == 1:
                        return "Fold"
                elif decision == 2:
                        return "Check"
                elif decision == 3:
                    while True:
                        bet = int(input(f" {player.nick} place your bet, type 'b' for going back: "))
                        if bet == 'b':
                                break
                        try:
                            if bet < self.minimal_bet:
                                print(f"You must bet at least {self.minimal_bet}")
                            elif bet > player.balance:
                                print("Insufficient balance.")
                            else:
                                return bet
                        except ValueError:
                            print(f"Invalid input, please enter number between minimal bet - {self.minimal_bet} and your balance - {player.balance}" ) #write what is minimal bet and balance
            except ValueError:
                print("Invalid input, please enetr number 1, 2 or 3")
    
    def play_betting(self, button):

        self.active_players = self.players.copy()
        current_player_index = (button + 3) % len(self.players)
        active_even_bet_count = 1

        while len(self.active_players) > 1 and active_even_bet_count < len(self.active_players):
            player = self.active_players[current_player_index]
            decision = self.bet_input(player)
            if decision == "Fold":
                player.fold()
                self.active_players.remove(player)
            elif decision == "Check":
                player.check()
                active_even_bet_count += 1
            else:
                bet = decision
                player.place_bet(bet)
                self.pot += bet 
                active_even_bet_count = 1
            current_player_index = (current_player_index + 1) % len(self.active_players)
        
        if len(self.active_players) == 1:
            self.active_players[0].receive_winnings(self.pot)
            print(f"{self.active_players[0].nick} has won {self.pot} pot")
            return True

    def play_community_cards(self, cards, number):
        for player in self.active_players:
            player.extend_with_dealer_cards(cards)
            hand_ev = HandEvaluator(player.cards)
            print(f"{player.nick} has {player.show_players_cards(number)} - {hand_ev.best_hand_name} with balance: {player.balance} ")

    def winner(self):                   #didnt test if it works, also dont have exception when there is all in and pot should be split to some players except all in in some range
        def concatenate_and_compare(hand1, hand2):
            hand1_c = (''.join(format(i, '02') for i in hand1))
            hand2_c = (''.join(format(i, '02') for i in hand2))
            print(hand1_c, hand2_c)
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
                best_hand = player_hand_evaluator
                winners = [player]
        
        for player in winners:
            player.receive_winnings(self.pot//len(winners))      


       
    def play(self, button = 0 ):
        self.dealer_draw()
        small_blind_player_index = (button + 1) % len(self.players)
        big_blind_player_index = (button + 2) % len(self.players)
        self.players[small_blind_player_index].place_bet(self.small_blind)
        self.players[big_blind_player_index].place_bet(self.big_blind)
        self.deal_players_cards()
        self.play_community_cards([], number = 2)
        if self.play_betting(button):
            return 
        print("Flop: ")
        self.show_flop()
        self.play_community_cards(self.dealer_cards[:3], number = 2)
        self.play_betting(button)
        print("Turn: ")
        self.show_turn()
        self.play_community_cards([self.dealer_cards[3]], number = 2 )
        self.play_betting(button)
        print("River: ")
        self.show_river()
        self.play_community_cards([self.dealer_cards[4]], number = 2)
        self.play_betting(button)
        self.winner()





p1 = Player("vibe")
p2 = Player("such")
p3 = Player("stah")
players = [p1,p2,p3]
hand = Game(players)
hand.play()

