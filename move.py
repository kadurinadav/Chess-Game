
class Move:

    def __init__(self, initial_sq, final_sq):
        self.initial_sq = initial_sq
        self.final_sq = final_sq

    def __eq__(self, other):
        """
            Check if two moves are equal      
        """
        return self.initial_sq == other.initial_sq and self.final_sq == other.final_sq