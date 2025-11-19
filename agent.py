import numpy as np
import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=1.0, 
                 epsilon_decay=0.9995, epsilon_min=0.01):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        self.training_stats = {
            'episodes': 0,
            'wins': 0,
            'losses': 0,
            'ties': 0
        }
    
    def get_state_key(self, state):
        if state is None:
            return None
        return tuple(state)
    
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 1)
        
        state_key = self.get_state_key(state)
        q_values = [self.q_table[state_key][0], self.q_table[state_key][1]]
        
        if q_values[0] == q_values[1]:
            return random.randint(0, 1)
        
        return np.argmax(q_values)
    
    def update_q_value(self, state, action, reward, next_state, done):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        current_q = self.q_table[state_key][action]
        
        if done:
            new_q = current_q + self.lr * (reward - current_q)
        else:
            max_next_q = max(self.q_table[next_state_key][0], 
                           self.q_table[next_state_key][1])
            new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        
        self.q_table[state_key][action] = new_q
    
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def train_episode(self, env):   
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = self.choose_action(state)
            next_state, reward, done = env.step(action)
            
            self.update_q_value(state, action, reward, next_state, done)
            
            total_reward += reward
            state = next_state
        
        self.training_stats['episodes'] += 1
        if reward == 1:
            self.training_stats['wins'] += 1
        elif reward == -1:
            self.training_stats['losses'] += 1
        else:
            self.training_stats['ties'] += 1
        
        self.decay_epsilon()
        return total_reward
    
    def train(self, env, num_episodes=100000):
        print(f"Training Q-Learning agent for {num_episodes} episodes...")
        print("="*60)
        
        rewards = []
        for episode in range(num_episodes):
            reward = self.train_episode(env)
            rewards.append(reward)
            
            if (episode + 1) % 10000 == 0:
                avg_reward = np.mean(rewards[-10000:])
                win_rate = self.training_stats['wins'] / self.training_stats['episodes'] * 100
                print(f"Episode {episode + 1}: "
                      f"Avg Reward: {avg_reward:.3f}, "
                      f"Win Rate: {win_rate:.2f}%, "
                      f"Epsilon: {self.epsilon:.3f}")
        
        print("\nTraining complete!")
        print(f"Final Win Rate: {self.training_stats['wins']/self.training_stats['episodes']*100:.2f}%")
        print(f"Final Loss Rate: {self.training_stats['losses']/self.training_stats['episodes']*100:.2f}%")
        print(f"Final Tie Rate: {self.training_stats['ties']/self.training_stats['episodes']*100:.2f}%")
    
    def test(self, env, num_episodes=1000):
        original_epsilon = self.epsilon
        self.epsilon = 0
        
        results = {'wins': 0, 'losses': 0, 'ties': 0}
        
        for _ in range(num_episodes):
            state = env.reset()
            done = False
            
            while not done:
                action = self.choose_action(state)
                next_state, reward, done = env.step(action)
                state = next_state
            
            if reward == 1:
                results['wins'] += 1
            elif reward == -1:
                results['losses'] += 1
            else:
                results['ties'] += 1
        
        self.epsilon = original_epsilon
        
        print(f"\n{'='*60}")
        print(f"TEST RESULTS ({num_episodes} episodes)")
        print(f"{'='*60}")
        print(f"Wins: {results['wins']} ({results['wins']/num_episodes*100:.2f}%)")
        print(f"Losses: {results['losses']} ({results['losses']/num_episodes*100:.2f}%)")
        print(f"Ties: {results['ties']} ({results['ties']/num_episodes*100:.2f}%)")
        
        return results
    
    def get_policy(self):
        policy = {}
        for state_key in self.q_table:
            action = np.argmax([self.q_table[state_key][0], 
                              self.q_table[state_key][1]])
            policy[state_key] = action
        
        return policy