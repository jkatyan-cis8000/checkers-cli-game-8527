from piece import Piece
from board import Board


def is_valid_move(board, from_row, from_col, to_row, to_col, current_player):
    if not _on_board(to_row, to_col):
        return False
    if board.get_piece(to_row, to_col) is not None:
        return False
    
    piece = board.get_piece(from_row, from_col)
    if piece is None or piece.color.upper() != current_player.upper():
        return False
    
    if not _is_diagonal(from_row, from_col, to_row, to_col):
        return False
    
    row_diff = to_row - from_row
    col_diff = to_col - from_col
    abs_row_diff = abs(row_diff)
    abs_col_diff = abs(col_diff)
    
    if abs_row_diff != abs_col_diff:
        return False
    
    if piece.is_king:
        return True
    
    if piece.color == 'red' and row_diff < 0:
        return False
    if piece.color == 'black' and row_diff > 0:
        return False
    
    return True


def _on_board(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def _is_diagonal(from_row, from_col, to_row, to_col):
    row_diff = to_row - from_row
    col_diff = to_col - from_col
    return row_diff != 0 and col_diff != 0


def can_capture(board, row, col, player):
    piece = board.get_piece(row, col)
    if piece is None or piece.color.upper() != player.upper():
        return False
    
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dr, dc in directions:
        mid_row = row + dr
        mid_col = col + dc
        dest_row = row + 2 * dr
        dest_col = col + 2 * dc
        
        if not _on_board(dest_row, dest_col):
            continue
        
        mid_piece = board.get_piece(mid_row, mid_col)
        dest_piece = board.get_piece(dest_row, dest_col)
        
        if mid_piece is not None and mid_piece.color.upper() != player.upper() and dest_piece is None:
            if piece.is_king or _is_forward(piece, dr):
                return True
    
    return False


def _is_forward(piece, row_diff):
    if piece.is_king:
        return True
    if piece.color == 'red' and row_diff < 0:
        return True
    if piece.color == 'black' and row_diff > 0:
        return True
    return False


def execute_move(board, from_row, from_col, to_row, to_col):
    piece = board.get_piece(from_row, from_col)
    board.remove_piece(from_row, from_col)
    board.place_piece(to_row, to_col, piece)
    
    row_diff = to_row - from_row
    col_diff = to_col - from_col
    
    if abs(row_diff) == 2 and abs(col_diff) == 2:
        mid_row = from_row + row_diff // 2
        mid_col = from_col + col_diff // 2
        board.remove_piece(mid_row, mid_col)
    
    if not piece.is_king:
        if piece.color == 'red' and to_row == 0:
            piece.is_king = True
        elif piece.color == 'black' and to_row == 8:
            piece.is_king = True


def has_valid_moves(board, player):
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is not None and piece.color.upper() == player.upper():
                if _has_any_valid_move(board, piece, row, col):
                    return True
    return False


def _has_any_valid_move(board, piece, row, col):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for dr, dc in directions:
        to_row = row + dr
        to_col = col + dc
        
        if _on_board(to_row, to_col) and board.get_piece(to_row, to_col) is None:
            if piece.is_king or _is_forward(piece, dr):
                return True
        
        dest_row = row + 2 * dr
        dest_col = col + 2 * dc
        
        if _on_board(dest_row, dest_col):
            mid_row = row + dr
            mid_col = col + dc
            mid_piece = board.get_piece(mid_row, mid_col)
            dest_piece = board.get_piece(dest_row, dest_col)
            
            if mid_piece is not None and mid_piece.color.upper() != piece.color.upper() and dest_piece is None:
                if piece.is_king or _is_forward(piece, dr):
                    return True
    
    return False
