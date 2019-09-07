class Character:
        
    def __init__(self, char, was_guessed = False):
        self.char = char.upper()
        self.was_guessed = was_guessed
        
    def update_guessed(self, guess):
        if self.was_guessed == False and guess == self.char:
            self.was_guessed = True
    
    def show_char(self):
        tile = '|{}'
        if self.was_guessed == True:
            return tile.format(self.char)
        else:
            return tile.format('_')