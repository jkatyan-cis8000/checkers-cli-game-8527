import re
from board import Board
from piece import Piece
from rules import Rules


class CheckersGame:
    """Main game controller for the checkers CLI game."""
    
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.game_over = False
        self.turn_count = 0
        self.move_history = []
    
    def play(self):
        """Main game loop."""
        print("Welcome to Checkers!")
        print("Enter moves in format: from_row,from_col to_row,to_col (e.g., 2,1 3,2)")
        print("Or 'quit' to exit.")
        print()
        
        self.board.display()
        
        while not self.game_over:
            print(f"\nPlayer {self.current_player}'s turn")
            move_input = input("Enter your move: ").strip()
            
            if move_input.lower() == 'quit':
                print("Game ended.")
                break
            
            if not self._process_move(move_input):
                continue
            
            self._check_game_over()
            self.current_player = 3 - self.current_player  # Switch between 1 and 2
            self.turn_count += 1
            self.board.display()
    
    def _process_move(self, move_input):
        """Parse and execute a move. Returns True if successful."""
        # Parse move: "row,col row,col" or "row,col to row,col"
        match = re.match(r'(\d),(\d)\s+(?:to\s+)?(\d),(\d)', move_input)
        if not match:
            print("Invalid format. Use: row,col row,col (e.g., 2,1 3,2)")
            return False
        
        from_row, from_col = int(match.group(1)), int(match.group(2))
        to_row, to_col = int(match.group(3)), int(match.group(4))
        
        # Validate move
        if not Rules.is_valid_move(self.board, from_row, from_col, to_row, to_col, self.current_player):
            print("Invalid move!")
            return False
        
        # Execute move
        Rules.execute_move(self.board, from_row, from_col, to_row, to_col)
        self.move_history.append((self.current_player, from_row, from_col, to_row, to_col))
        
        return True
    
    def _check_game_over(self):
        """Check if game has ended."""
        # Check if current player has valid moves
        if not Rules.has_valid_moves(self.board, self.current_player):
            winner = 3 - self.current_player
            print(f"\nPlayer {winner} wins! Player {self.current_player} has no valid moves.")
            self.game_over = True
            return
        
        # Check for simple win condition (opponent has no pieces)
        player1_count = sum(1 for row in self.board.grid for p in row if p and p.color == '1')
        player2_count = sum(1 for row in self.board.grid for p in row if p and p.color == '2')
        
        if player1_count == 0:
            print("\nPlayer 2 wins! Player 1 has no pieces left.")
            self.game_over = True
        elif player2_count == 0:
            print("\nPlayer 1 wins! Player 2 has no pieces left.")
            self.game_over = True
    
    def get_state(self):
        """Return current game state as dict."""
        return {
            'current_player': self.current_player,
            'turn_count': self.turn_count,
            'game_over': self.game_over,
            'board': [[p.to_dict() if p else None for p in row] for row in self.board.grid]
        }


def main():
    game = CheckersGame()
    game.play()


if __name__ == '__main__':
    main()
