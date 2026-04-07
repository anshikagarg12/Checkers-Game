import numpy as np
import random
class CheckersEnv:
    # Add this below your get_board(self) function
    def make_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # 1. Identify which piece is moving
        piece = self.board[start_row][start_col]
        
        # 2. Place the piece in the new empty square
        self.board[end_row][end_col] = piece
        
        # 3. Remove the piece from the old square
        self.board[start_row][start_col] = 0
        
        # For now, we allow ALL moves (we will add rules later!)
        return True
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