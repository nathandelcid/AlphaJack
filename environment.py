from blackjack import BlackjackGame

class Environment:
    def __init__(self, num_decks=6):
        self.game = BlackjackGame(num_decks)
        self.reset()
    
    def reset(self):
        self.game.deal_initial_cards()
        return self.get_state()
    
    def get_state(self):
        player_value = self.game.player_hand.get_value()
        dealer_card = self.game.dealer_hand.cards[0].value()[0]
        usable_ace = self._has_usable_ace(self.game.player_hand)
        return (player_value, dealer_card, usable_ace)
    
    def _has_usable_ace(self, hand):
        ace_count = sum(1 for card in hand.cards if card.rank == 'A')
        if ace_count == 0:
            return False
        base_value = sum(card.value()[0] for card in hand.cards if card.rank != 'A')
        return base_value + 11 + (ace_count - 1) <= 21
    
    def step(self, action):
        done = False
        reward = 0
        
        if action == 0:
            self.game.player_hit()
            if self.game.player_hand.is_bust():
                done = True
                reward = -1
        else:
            done = True
            self.game.dealer_play()
            winner, _ = self.game.determine_winner()
            if winner == 'player':
                reward = 1
            elif winner == 'dealer':
                reward = -1
            else:
                reward = 0
        
        next_state = self.get_state() if not done else None
        return next_state, reward, done


