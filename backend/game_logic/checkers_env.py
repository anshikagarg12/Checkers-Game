import numpy as np
import random

class CheckersEnv:
    def __init__(self):
        # Initialize an 8x8 grid with zeros
        self.board = np.zeros((8, 8), dtype=int)
        
        # 1 will be Player 1 (Bottom), -1 will be Player 2 (Top)
        self.current_player = 1 
        self.setup_board()

    def setup_board(self):
        # Place Player 2 (-1) pieces on the top 3 rows (dark squares)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 != 0:
                    self.board[row][col] = -1
        
        # Place Player 1 (1) pieces on the bottom 3 rows (dark squares)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    self.board[row][col] = 1

    def get_board(self):
        # Convert the NumPy array to a standard Python list 
        # so Flask can easily send it over the internet as JSON
        return self.board.tolist()
    def is_valid_move(self, start_pos, end_pos, player):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # 1. EDGE DETECTION: Stop the piece from falling off the board
        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            return False
        
        # 2. The destination MUST be an empty square
        if self.board[end_row][end_col] != 0:
            return False
            
        row_diff = end_row - start_row
        col_diff = abs(end_col - start_col)
        
        # 3. Determine allowed forward directions
        allowed_row_diffs = []
        if player == 1: allowed_row_diffs = [-1]         # Red moves Up
        elif player == -1: allowed_row_diffs = [1]       # White moves Down
        elif abs(player) == 2: allowed_row_diffs = [-1, 1] # Kings move Both Ways!
        
        # 4. NORMAL MOVES (1 step)
        if col_diff == 1 and row_diff in allowed_row_diffs:
            return True
            
        # 5. CAPTURE MOVES (2 steps)
        if col_diff == 2 and (row_diff // 2) in allowed_row_diffs:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            mid_piece = self.board[mid_row][mid_col]
            
            # Make sure we are jumping over an ENEMY piece
            if player in [1, 2] and mid_piece in [-1, -2]: 
                return True
            if player in [-1, -2] and mid_piece in [1, 2]: 
                return True
                
        return False
    def make_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]
        
        if self.is_valid_move(start_pos, end_pos, piece):
            # Execute the move
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = 0
            reward = 0 
            
            # Was it a capture?
            if abs(end_row - start_row) == 2:
                mid_row = (start_row + end_row) // 2
                mid_col = (start_col + end_col) // 2
                self.board[mid_row][mid_col] = 0
                reward = 10 
                
            # KINGING LOGIC: If a piece hits the opposite edge, promote it!
            if piece == 1 and end_row == 0:
                self.board[end_row][end_col] = 2  # Promote to Red King
                reward += 5 # RL bonus for getting a king
            elif piece == -1 and end_row == 7:
                self.board[end_row][end_col] = -2 # Promote to White King
                
            return True, reward
            
        return False, -10

    def make_computer_move(self):
        valid_moves = []
        capture_moves = []
        
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                # Look for computer pieces (both normal -1 and king -2)
                if piece in [-1, -2]: 
                    
                    # Test all 4 diagonal directions
                    for dr in [-1, 1]:
                        for dc in [-1, 1]:
                            # Test 1-step move
                            if self.is_valid_move((r, c), (r + dr, c + dc), piece):
                                valid_moves.append(((r, c), (r + dr, c + dc)))
                            # Test 2-step capture
                            if self.is_valid_move((r, c), (r + dr*2, c + dc*2), piece):
                                capture_moves.append(((r, c), (r + dr*2, c + dc*2)))
                                
        if capture_moves:
            chosen_move = random.choice(capture_moves)
        elif valid_moves:
            chosen_move = random.choice(valid_moves)
        else:
            return 

        self.make_move(chosen_move[0], chosen_move[1])
    def check_winner(self):
        """
        Scans the board. Returns 1 if Player wins, -1 if Computer wins, 
        and 0 if the game is still going.
        """
        # Count how many pieces each player has left on the board
        p1_pieces = np.sum((self.board == 1) | (self.board == 2))
        comp_pieces = np.sum((self.board == -1) | (self.board == -2))
        
        if p1_pieces == 0:
            return -1 # Computer annihilated the player
            
        if comp_pieces == 0:
            return 1 # Player annihilated the computer
            
        return 0 # Game is still going!