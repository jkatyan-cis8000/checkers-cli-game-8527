from piece import Piece


class Rules:
    """Game rules for checkers including move validation, captures, and kinging."""
    
    @staticmethod
    def is_valid_move(board, from_row, from_col, to_row, to_col, current_player):
        """
        Check if a move is valid according to standard checkers rules.
        Returns True if valid, False otherwise.
        """
        # Get the piece
        piece = board.get_piece(from_row, from_col)
        if piece is None:
            return False
        
        # Player must match
        if piece.color != str(current_player):
            return False
        
        # Destination must be empty
        if board.get_piece(to_row, to_col) is not None:
            return False
        
        # Check if move is on a diagonal
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        if row_diff != col_diff:
            return False
        
        # Regular piece moves forward only
        if not piece.is_king:
            if piece.color == '1':  # Player 1 moves up (row decreases)
                if to_row >= from_row:
                    return False
            else:  # Player 2 moves down (row increases)
                if to_row <= from_row:
                    return False
        
        # Check distance (1 for normal move, 2 for capture)
        if row_diff == 1:
            return True  # Valid single step
        elif row_diff == 2:
            return Rules._is_valid_capture(board, from_row, from_col, to_row, to_col)
        else:
            return False  # Too far
    
    @staticmethod
    def _is_valid_capture(board, from_row, from_col, to_row, to_col):
        """Check if this is a valid capture move."""
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        
        mid_piece = board.get_piece(mid_row, mid_col)
        if mid_piece is None:
            return False
        
        # Must capture opponent
        from_piece = board.get_piece(from_row, from_col)
        if from_piece.color == mid_piece.color:
            return False
        
        return True
    
    @staticmethod
    def execute_move(board, from_row, from_col, to_row, to_col):
        """
        Execute a move and return capture information.
        Returns (piece_moved, captured_piece) where captured_piece may be None.
        """
        piece = board.get_piece(from_row, from_col)
        
        # Check if it's a capture
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        captured = None
        
        if row_diff == 2:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            captured = board.get_piece(mid_row, mid_col)
            board.remove_piece(mid_row, mid_col)
        
        board.move_piece(from_row, from_col, to_row, to_col)
        
        # Check for kinging
        if piece.color == '1' and to_row == 0:
            piece.is_king = True
        elif piece.color == '2' and to_row == 7:
            piece.is_king = True
        
        return piece, captured
    
    @staticmethod
    def get_valid_moves(board, row, col):
        """Get all valid moves for a piece at position."""
        piece = board.get_piece(row, col)
        if piece is None:
            return []
        
        moves = []
        
        # Determine direction(s) piece can move
        directions = []
        if piece.color == '1' or piece.is_king:  # Player 1 (up) or king
            directions.append((-1, -1))  # Up-left
            directions.append((-1, 1))   # Up-right
        if piece.color == '2' or piece.is_king:  # Player 2 (down) or king
            directions.append((1, -1))   # Down-left
            directions.append((1, 1))    # Down-right
        
        # Check single steps
        for dr, dc in directions:
            to_row, to_col = row + dr, col + dc
            if Rules._is_on_board(to_row, to_col) and board.get_piece(to_row, to_col) is None:
                moves.append((to_row, to_col))
        
        # Check captures
        for dr, dc in directions:
            jump_row, jump_col = row + 2 * dr, col + 2 * dc
            if Rules._is_on_board(jump_row, jump_col) and board.get_piece(jump_row, jump_col) is None:
                mid_row, mid_col = row + dr, col + dc
                mid_piece = board.get_piece(mid_row, mid_col)
                if mid_piece is not None and mid_piece.color != piece.color:
                    moves.append((jump_row, jump_col))
        
        return moves
    
    @staticmethod
    def _is_on_board(row, col):
        """Check if position is within board bounds."""
        return 0 <= row < 8 and 0 <= col < 8
    
    @staticmethod
    def has_valid_moves(board, player):
        """Check if a player has any valid moves."""
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece is not None and piece.color == str(player):
                    if Rules.get_valid_moves(board, row, col):
                        return True
        return False
    
    @staticmethod
    def get_captured_positions(board, from_row, from_col, to_row, to_col):
        """Get list of positions captured in a move (for multi-jump support)."""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        captured = []
        
        if row_diff == 2:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            mid_piece = board.get_piece(mid_row, mid_col)
            if mid_piece is not None:
                captured.append((mid_row, mid_col))
        
        return captured
