import logging
import os
from phrasehunter.phrase import Phrase
from datetime import datetime
from random import choice, randint

logging.basicConfig(filename = 'app.log', level = logging.DEBUG)

class Game:
    
    APP_NAME = 'Phrase Hunter'
    
    def __init__(self, phrases, game_on = True):
        self.phrases = [Phrase(phrase) for phrase in phrases]
        self.hints = [hint.title() for hint in phrases.values()]
        self.game_on = game_on
        self.guessed_phrases_idx = []

    def choose_active(self):
        self.idx = randint(0, len(self.phrases) - 1)
        if len(self.guessed_phrases_idx) == len(self.phrases):  # check if user has gone through all available phrases
            self.guessed_phrases_idx = []
            for phrase in self.phrases:
                phrase.reset_phrase()
        else:
            while self.idx in self.guessed_phrases_idx:  # random selection should not return already guessed phrase
                self.idx = randint(0, len(self.phrases) - 1)
        self.active = self.phrases[self.idx]
        self.hint = self.hints[self.idx]
        self.guessed_letters = []
        self.lives = 5
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self, text):
        print('#'*(len(text) + 6))
        print('##', text, '##')
        print('#'*(len(text) + 6))
        print()
    
    def display_menu(self, message):
        print(message)
        return input("Enter an option > ")
    
    def invalid_entry(self, entry):
        self.clear_screen()
        print(f"\nWhoops! [{entry}] is an unexpected entry!\n")
        print()
    
    def get_guess(self):
        right_guess = False
        guess = input("Enter a single character > ").upper()
        self.clear_screen()
        if len(guess) > 1:
            print("\nWhoops! Guess can be only be 1 character in length")
        elif not guess.isalpha():
            print("\nWhoops! Guess can be only be a letter character: a through z (uppercase or lowercase)")
        elif guess in self.guessed_letters:
            print(f"\nWhoops! Letter [{guess}] was already tried before. Please try a different letter!\n")
        elif not self.active.letter_exists(guess):
            print(f"\nWhoops! Letter [{guess}] does not exist in phrase. Please try a different letter!\n")
            self.lives -= 1
            self.guessed_letters.append(guess)
        else:
            self.active.check_guess(guess)
            self.guessed_letters.append(guess)
            right_guess = True
        return right_guess
    
    
    def end_game(self):
        self.clear_screen()
        self.print_title(f"Thank you for using {self.APP_NAME}!")
        logging.info(f"{datetime.today()}: Game Ended")
        self.game_on = False
    
    def play_again(self):
        while True:
            option_selected = self.display_menu("""\nWould you like to play again?:
    
    [Y]   To restart the game
    [N]   To end the game
    
    """)
            if option_selected.upper() == 'Y':
                self.clear_screen()
                self.choose_active()
                break
            elif option_selected.upper() == 'N':
                self.end_game()
                break
            else:
                self.clear_screen()
                print(f"\nWhoops! [{option_selected}] is not a valid entry\n")
                continue
            
    
    def start_game(self):
        logging.info(f"{datetime.today()}: Game Started")
        self.clear_screen()
        while self.game_on:
            self.print_title(f"Welcome to {self.APP_NAME}")
            self.choose_active()
            while self.lives:
                print(f'\nHINT: {self.hint}')
                self.active.show_phrase()
                print(f"\nYou have {self.lives} lives remaining")
                print()
                right_guess = self.get_guess()
                if right_guess:
                    if self.active.entirely_guessed():
                        self.guessed_phrases_idx.append(self.idx)
                        self.clear_screen()
                        self.print_title("CONGRATULATIONS! YOU GUESSED THE ENTIRE PHRASE!")
                        self.active.show_phrase()
                        self.play_again()
                elif not self.lives:
                    self.clear_screen()
                    self.print_title("Sorry, you ran out of guesses :(")
                    self.active.show_phrase()
                    self.play_again()
                else:
                    continue