class Piece:
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king

    def __repr__(self):
        color_str = str(self.color)
        if self.is_king:
            return color_str.upper() + 'K'
        return color_str.upper()

    def to_dict(self):
        return {"color": self.color, "is_king": self.is_king}
