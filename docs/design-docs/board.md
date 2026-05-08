# Board Module Design Doc

## Overview
The Board class implements an 8x8 Checkers game board with piece placement, movement, and display capabilities.

## Implementation Details

### Class: Board
- **Location**: `src/board.py`
- **Purpose**: Manages the game state and piece positions

### Attributes
- `grid`: 8x8 list of lists containing Piece objects or None

### Methods

#### `__init__`
- Initializes 8x8 grid with None values
- Calls `_initialize_pieces()` to set up standard Checkers starting position
- Places 12 red pieces (rows 0-2) and 12 black pieces (rows 5-7)

#### `__repr__`
- Returns string representation: `Board(8x8)`

#### `place_piece(row, col, piece)`
- Places a Piece object at the specified position

#### `get_piece(row, col)`
- Returns the Piece at the specified position (or None)

#### `remove_piece(row, col)`
- Removes the piece at the specified position

#### `move_piece(from_row, from_col, to_row, to_col)`
- Moves piece from one position to another

#### `display()`
- Prints the board to stdout
- Shows '.' for empty squares
- Shows 'R'/'B' for regular pieces, 'RK'/'BK' for kings

### Design Decisions

1. **Piece Storage**: Uses list of lists for O(1) access to any square
2. **Piece Representation**: Relies on Piece class from piece.py for piece state
3. **Display Format**: Simple text output for CLI environment
4. **No Validation**: Board class doesn't validate moves - that's game logic's responsibility
