from phrasehunter.character import Character

class Phrase:
    
    def __init__(self, phrase):
        self.phrase = [Character(char) for char in phrase]
        
    def entirely_guessed(self):
        for char in self.phrase:
            if char.was_guessed == False:
                return False
        return True
    
    def check_guess(self, guess):
        for char in self.phrase:
            char.update_guessed(guess)

    def show_phrase(self):
        print(' _' * len(self.phrase))
        for char in self.phrase:
            print(char.show_char(), end='')
        print('|')
        
    def letter_exists(self, guess):
        for char in self.phrase:
            if char.char == guess:
                return True
        return False
    
    def reset_phrase(self):
        for char in self.phrase:
            char.was_guessed = False
