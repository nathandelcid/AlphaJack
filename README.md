# AlphaJack: Blackjack Q-Learning Agent

## Overview

Here we are analyzing the performance of a RL agent trained to play Blackjack using Q-Learning. The agent learns optimal playing strategies through experience, discovering when to hit or stand based on the current state.

### Key Components

1. **Environment** (`environment.py`): Wraps the Blackjack game into a standard RL environment with state representation and reward structure
2. **Agent** (`agent.py`): Implements Q-Learning algorithm with epsilon-greedy exploration
3. **Blackjack Game** (`blackjack.py`): Provides the core game mechanics including card dealing, hand evaluation, and winner determination

### Q-Learning Algorithm

Q-Learning is a model-free, off-policy reinforcement learning algorithm that learns the value of actions in specific states. The agent maintains a Q-table where each entry $Q(s,a)$ represents the expected cumulative reward for taking action *$a$* in state *$s$*.

$$
Q_{t+1}(s,a) = Q_t(s,a) + \alpha \Bigl[r + \gamma \max_{a'} Q_t(s',a') - Q_t(s,a)\Bigr]
$$

- $\alpha$: Learning rate
- $\gamma$: Discount factor  
- $r$: Immediate reward
- $s'$: Next state

### State Representation

Each state is represented as a 3-tuple:
- **Player hand value** (4-21): Current sum of player's cards
- **Dealer's showing card** (1-10): The dealer's visible card
- **Usable ace** (True/False): Whether player has an ace counted as 11

### Action Space

- **Action 0**: Hit (draw another card)
- **Action 1**: Stand (end turn)

### Reward Structure

- **+1**: Player wins
- **-1**: Player loses
- **0**: Push (tie)