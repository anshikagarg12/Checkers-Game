from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import random # <--- ADD THIS AT THE TOP
# Import the environment we just built
from game_logic.checkers_env import CheckersEnv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/', methods=['GET'])
def home():
    return "Flask is running! The game data is located at /api/game/start"
# We will store the active game here in memory for now
game_session = CheckersEnv()

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "success",
        "message": "Flask backend is up and running!"
    })

# We changed this to a GET request so React can easily fetch it on page load
@app.route('/api/game/start', methods=['GET'])
def start_game():
    global game_session
    game_session = CheckersEnv()  # This resets the board to the starting position
    
    return jsonify({
        "status": "game_started",
        "board": game_session.get_board(),
        "current_player": game_session.current_player
    })
# We use POST here because React is sending us data (the coordinates)
@app.route('/api/game/move', methods=['POST'])
def move_piece():
    global game_session
    
    data = request.json
    start_pos = data.get('start')
    end_pos = data.get('end')
    
    # 1. Player makes their move
    game_session.make_move(start_pos, end_pos)
    
    # 2. AI automatically makes its move instantly!
    game_session.make_computer_move()
    
    # 3. Send the updated board back to React
    return jsonify({
        "status": "success",
        "board": game_session.get_board()
    })
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)




class CheckersEnv:
    # ... (keep your __init__, setup_board, get_board, and make_move) ...

    # ADD THIS AT THE BOTTOM
    def make_computer_move(self):
        """
        This is a PLACEHOLDER for your future Reinforcement Learning Agent.
        Right now, it just picks a random white piece and teleports it to a random empty square.
        Eventually, this function will pass the board to a Neural Network to pick the best move.
        """
        # 1. Find all computer pieces (-1)
        computer_pieces = []
        empty_squares = []
        
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == -1:
                    computer_pieces.append((r, c))
                # Only look for empty dark squares
                elif self.board[r][c] == 0 and (r + c) % 2 != 0:
                    empty_squares.append((r, c))
                    
        # 2. If the computer has pieces and there is space, make a random move
        if computer_pieces and empty_squares:
            start_pos = random.choice(computer_pieces)
            end_pos = random.choice(empty_squares)
            
            # Execute the move
            self.make_move(start_pos, end_pos)