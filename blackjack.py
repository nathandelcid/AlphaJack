import random
from typing import List, Tuple

class Card:
    
    SUITS = ['♠', '♥', '♦', '♣']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def value(self) -> List[int]:
        if self.rank in ['J', 'Q', 'K']:
            return [10]
        elif self.rank == 'A':
            return [1, 11]
        else:
            return [int(self.rank)]


class Deck:
    
    def __init__(self, num_decks: int = 1):
        self.cards = []
        self.num_decks = num_decks
        self.reset()
    
    def reset(self):
        self.cards = []
        for _ in range(self.num_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    self.cards.append(Card(rank, suit))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        if len(self.cards) == 0:
            self.reset()
        return self.cards.pop()


class Hand:
    
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def get_value(self) -> int:
        values = [0]
        
        for card in self.cards:
            new_values = []
            for val in values:
                for card_val in card.value():
                    new_values.append(val + card_val)
            values = new_values
        
        valid_values = [v for v in values if v <= 21]
        if valid_values:
            return max(valid_values)
        else:
            return min(values)
    
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self) -> bool:
        return self.get_value() > 21
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards) + f" (Value: {self.get_value()})"


class BlackjackGame:
    
    def __init__(self, num_decks: int = 6):
        self.deck = Deck(num_decks)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
    
    def deal_initial_cards(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        
        for _ in range(2):
            self.player_hand.add_card(self.deck.draw())
            self.dealer_hand.add_card(self.deck.draw())
    
    def player_hit(self) -> bool:
        self.player_hand.add_card(self.deck.draw())
        if self.player_hand.is_bust():
            self.game_over = True
            return False
        return True
    
    def dealer_play(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())
    
    def determine_winner(self) -> Tuple[str, str]:
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        if self.player_hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            return ('player', 'Blackjack! Player wins!')
        elif self.dealer_hand.is_blackjack() and not self.player_hand.is_blackjack():
            return ('dealer', 'Dealer has Blackjack! Dealer wins!')
        elif self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            return ('tie', 'Both have Blackjack! Push (Tie)!')
        elif self.player_hand.is_bust():
            return ('dealer', f'Player busts with {player_value}! Dealer wins!')
        elif self.dealer_hand.is_bust():
            return ('player', f'Dealer busts with {dealer_value}! Player wins!')
        elif player_value > dealer_value:
            return ('player', f'Player wins with {player_value} vs {dealer_value}!')
        elif dealer_value > player_value:
            return ('dealer', f'Dealer wins with {dealer_value} vs {player_value}!')
        else:
            return ('tie', f'Push (Tie) at {player_value}!')
    
    def play_round(self, strategy='interactive') -> str:
        self.deal_initial_cards()
        
        print("\n" + "="*50)
        print("NEW ROUND")
        print("="*50)
        print(f"Dealer shows: {self.dealer_hand.cards[0]}")
        print(f"Your hand: {self.player_hand}")
        
        if self.player_hand.is_blackjack() or self.dealer_hand.is_blackjack():
            print(f"\nDealer's hand: {self.dealer_hand}")
            result, message = self.determine_winner()
            print(message)
            return result
        
        if strategy == 'interactive':
            while not self.game_over:
                action = input("\n(H)it or (S)tand? ").strip().lower()
                if action in ['h', 'hit']:
                    self.player_hit()
                    print(f"Your hand: {self.player_hand}")
                    if self.player_hand.is_bust():
                        break
                elif action in ['s', 'stand']:
                    break
                else:
                    print("Invalid input. Please enter H or S.")
        elif strategy == 'dealer':
            while self.player_hand.get_value() < 17 and not self.game_over:
                print("Player hits...")
                self.player_hit()
                print(f"Your hand: {self.player_hand}")
        
        if self.player_hand.is_bust():
            print(f"\nDealer's hand: {self.dealer_hand}")
            result, message = self.determine_winner()
            print(message)
            return result
        
        print(f"\nDealer's hand: {self.dealer_hand}")
        print("Dealer plays...")
        self.dealer_play()
        print(f"Dealer's final hand: {self.dealer_hand}")
        
        result, message = self.determine_winner()
        print(message)
        return result


def simulate_games(num_games: int = 1000, strategy: str = 'dealer'):
    game = BlackjackGame()
    results = {'player': 0, 'dealer': 0, 'tie': 0}
    
    for i in range(num_games):
        result = game.play_round(strategy)
        results[result] += 1
    
    print(f"\n{'='*50}")
    print(f"SIMULATION RESULTS ({num_games} games)")
    print(f"{'='*50}")
    print(f"Player wins: {results['player']} ({results['player']/num_games*100:.1f}%)")
    print(f"Dealer wins: {results['dealer']} ({results['dealer']/num_games*100:.1f}%)")
    print(f"Ties: {results['tie']} ({results['tie']/num_games*100:.1f}%)")
    
    return results


if __name__ == "__main__":
    print("Welcome to Blackjack Simulator!")
    print("\nOptions:")
    print("1. Play interactively")
    print("2. Run simulation (1000 games)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == '1':
        game = BlackjackGame()
        wins = {'player': 0, 'dealer': 0, 'tie': 0}
        
        while True:
            result = game.play_round('interactive')
            wins[result] += 1
            
            print(f"\nCurrent record - Wins: {wins['player']}, Losses: {wins['dealer']}, Ties: {wins['tie']}")
            
            play_again = input("\nPlay another round? (y/n): ").strip().lower()
            if play_again not in ['y', 'yes']:
                break
        
        print("\nThanks for playing!")
    elif choice == '2':
        simulate_games(1000, 'dealer')
    else:
        print("Invalid choice!")