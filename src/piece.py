class Piece:
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king
    
    def __repr__(self):
        if self.is_king:
            return self.color.upper() + 'K'
        return self.color.upper()
