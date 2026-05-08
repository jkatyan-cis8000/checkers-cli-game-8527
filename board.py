from piece import Piece


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self._initialize_pieces()
    
    def _initialize_pieces(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.grid[row][col] = Piece(2)
                    elif row > 4:
                        self.grid[row][col] = Piece(1)
    
    def __repr__(self):
        return f"Board({len(self.grid)}x{len(self.grid[0])})"
    
    def place_piece(self, row, col, piece):
        self.grid[row][col] = piece
    
    def get_piece(self, row, col):
        return self.grid[row][col]
    
    def remove_piece(self, row, col):
        self.grid[row][col] = None
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.grid[from_row][from_col]
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
    
    def display(self):
        for row in range(8):
            line = ''
            for col in range(8):
                piece = self.grid[row][col]
                if piece is None:
                    if (row + col) % 2 == 0:
                        line += '. '
                    else:
                        line += '. '
                else:
                    if piece.is_king:
                        line += repr(piece) + ' '
                    else:
                        line += repr(piece) + ' '
            print(line)
