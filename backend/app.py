from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing to allow React to communicate with Flask
CORS(app)

# A simple route to test the connection
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "success",
        "message": "Flask backend is up and running!"
    })

# A placeholder route for starting a new game later
@app.route('/api/game/start', methods=['POST'])
def start_game():
    # TODO: Import CheckersEnv, initialize a new board, and return the state
    return jsonify({
        "status": "game_started",
        "board": [] # We will pass the np.zeros board here later
    })

if __name__ == '__main__':
    # Run the server in debug mode on port 5000
    app.run(debug=True, port=5000)
    