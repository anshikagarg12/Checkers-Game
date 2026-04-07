# backend/train_agent.py
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import copy
from collections import deque
from game_logic.checkers_env import CheckersEnv

# 1. The Brain: A Deep Neural Network
class CheckersBrain(nn.Module):
    def __init__(self):
        super(CheckersBrain, self).__init__()
        # The board is 8x8, so 64 inputs
        self.fc1 = nn.Linear(64, 128)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 128)
        self.relu2 = nn.ReLU()
        # Output is 1 number: The "Score" of how good this board is for the computer
        self.fc3 = nn.Linear(128, 1)

    def forward(self, x):
        # Flatten the 8x8 board into a 1D array of 64 numbers
        x = x.view(x.size(0), -1) 
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        x = self.fc3(x)
        return x

# 2. The Memory: So the AI can learn from past games
class ReplayMemory:
    def __init__(self, capacity=10000):
        self.memory = deque(maxlen=capacity)

    def push(self, state, reward, next_state, done):
        self.memory.append((state, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

print("Brain and Memory successfully initialized!")
# --- Add this below your ReplayMemory class ---

class DQNAgent:
    def __init__(self):
        # The Brain that learns
        self.policy_net = CheckersBrain()
        # The optimizer that tweaks the neurons based on rewards
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.001)
        self.memory = ReplayMemory(10000)
        self.epsilon = 1.0  # Start 100% random
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

    def get_all_valid_moves(self, env, player):
        """Helper to find all legal moves for a specific player"""
        valid_moves = []
        capture_moves = []
        target_pieces = [-1, -2] if player == -1 else [1, 2]
        
        for r in range(8):
            for c in range(8):
                piece = env.board[r][c]
                if piece in target_pieces:
                    for dr in [-1, 1]:
                        for dc in [-1, 1]:
                            if env.is_valid_move((r, c), (r + dr, c + dc), piece):
                                valid_moves.append(((r, c), (r + dr, c + dc)))
                            if env.is_valid_move((r, c), (r + dr*2, c + dc*2), piece):
                                capture_moves.append(((r, c), (r + dr*2, c + dc*2)))
                                
        # Always prioritize captures if available!
        return capture_moves if capture_moves else valid_moves

    def select_move(self, env, player):
        valid_moves = self.get_all_valid_moves(env, player)
        if not valid_moves:
            return None
            
        # 1. EXPLORE: Roll the dice, make a random move
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
            
        # 2. EXPLOIT: Use the Neural Network to pick the best move
        best_move = None
        best_score = -float('inf')
        
        for move in valid_moves:
            # Create a clone of the board to "look into the future"
            sim_env = copy.deepcopy(env)
            sim_env.make_move(move[0], move[1])
            
            # Convert the future board into numbers for PyTorch
            board_tensor = torch.FloatTensor(sim_env.board).unsqueeze(0)
            
            # Ask the Brain: "How good is this future board for me?"
            with torch.no_grad():
                score = self.policy_net(board_tensor).item()
                
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    # --- Add this at the very bottom of train_agent.py ---

def train_ai():
    env = CheckersEnv()
    agent = DQNAgent()
    
    # Let's train it for 100 fast-forward games to start
    EPISODES = 100 
    
    print("Starting Training inside the Hyperbolic Time Chamber...")
    
    for episode in range(EPISODES):
        env = CheckersEnv() # Reset board
        done = False
        total_reward = 0
        
        while not done:
            # 1. Player 1 (Random Dummy) moves
            p1_moves = agent.get_all_valid_moves(env, 1)
            if not p1_moves:
                break # P1 got stuck
            move1 = random.choice(p1_moves)
            env.make_move(move1[0], move1[1])
            
            if env.check_winner() != 0:
                break
                
            # 2. Computer (Our AI Agent) moves
            move2 = agent.select_move(env, -1)
            if not move2:
                break # AI got stuck
                
            # Execute the AI's move and get the reward!
            _, reward = env.make_move(move2[0], move2[1])
            total_reward += reward
            
            if env.check_winner() != 0:
                break
                
        # At the end of every game, reduce epsilon so it stops moving randomly
        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay
            
        # Print progress every 10 games
        if (episode + 1) % 10 == 0:
            print(f"Game {episode + 1}/{EPISODES} | AI Total Reward: {total_reward} | Epsilon (Randomness): {agent.epsilon:.2f}")

    print("Training Complete! Saving Brain...")
    torch.save(agent.policy_net.state_dict(), "checkers_brain.pth")
    print("Brain saved as 'checkers_brain.pth'!")

if __name__ == "__main__":
    train_ai()