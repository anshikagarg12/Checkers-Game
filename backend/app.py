# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import torch

# Import your game environment AND your new PyTorch Agent
from game_logic.checkers_env import CheckersEnv
from train_agent import DQNAgent 

app = Flask(__name__)
CORS(app)

game_session = CheckersEnv()

# --- 1. WAKE UP THE AI ---
print("Waking up the Neural Network...")
ai_agent = DQNAgent()

try:
    # Load the memories from the .pth file!
    ai_agent.policy_net.load_state_dict(torch.load("checkers_brain.pth", weights_only=True))
    ai_agent.policy_net.eval() # Lock the brain into "Playing" mode (stop learning)
    ai_agent.epsilon = 0.0 # 0% Randomness, 100% Try-Hard Mode
    print("🧠 PyTorch AI Brain loaded successfully!")
except Exception as e:
    print(f"⚠️ Could not load AI brain. Did you run train_agent.py? Error: {e}")


@app.route('/api/game/start', methods=['GET'])
def start_game():
    global game_session
    game_session = CheckersEnv()
    return jsonify({
        "status": "game_started",
        "board": game_session.get_board()
    })


@app.route('/api/game/move', methods=['POST'])
def move_piece():
    global game_session, ai_agent
    
    data = request.json
    start_pos = data.get('start')
    end_pos = data.get('end')
    
    # 1. Player makes their move
    success, reward = game_session.make_move(start_pos, end_pos)
    winner = game_session.check_winner()
    
    # 2. THE SMART AI TAKES ITS TURN
    if winner == 0 and success:
        
        # Ask PyTorch to simulate all futures and pick the best move!
        best_move = ai_agent.select_move(game_session, -1)
        
        if best_move:
            game_session.make_move(best_move[0], best_move[1])
            
        winner = game_session.check_winner()
    
    # 3. Send the board back to React
    status_message = "success" if winner == 0 else "game_over"
    
    return jsonify({
        "status": status_message,
        "winner": winner,
        "board": game_session.get_board()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)