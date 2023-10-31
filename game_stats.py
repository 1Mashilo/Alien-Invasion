import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score_file = 'high_score.json'
        self.load_high_score() 
        self.new_high_score = False 

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        """Load the high score from a file or set it to 0 if the file doesn't exist."""
        try:
            with open(self.high_score_file, 'r') as file:
                self.high_score = json.load(file)
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        """Save the high score to a file."""
        with open(self.high_score_file, 'w') as file:
            json.dump(self.high_score, file)

    def check_high_score(self):
        """Check if the current score is a new high score."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_high_score = True
            self.save_high_score()

    def reset_new_high_score(self):
        """Reset the new high score flag."""
        self.new_high_score = False


