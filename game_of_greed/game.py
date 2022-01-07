
from game_of_greed.game_logic import GameLogic
from game_of_greed.banker import Banker 
from textwrap import dedent
import sys

class Game:

    def __init__(self):
        self.round = 1
        self.banker = Banker()
        self.num_dice = 6
        
    def play(self, roller = GameLogic.roll_dice):
        starting = self.start_game()
        if starting:  
            while True:
                roll = self.roll_dice(roller)
                #choose dice and validate choice
                keepers = self.choose_and_validate_keepers(roll)
                if keepers == 'ZILCH': 
                    #goes to next round if no possible points
                    self.print_zilch_msg()
                    self.end_round()
                    continue 
                self.shelf_points(keepers)
                #choose to bank, quit, or roll again
                selection = input('> ')
                if selection.lower() == 'b':
                    self.end_round(True) #True arg means to bank at end of round
                elif selection.lower() == 'q':
                    self.exit_game()
                elif selection.lower() == 'r' and self.num_dice == 0:
                    self.num_dice = 6
        else:
            print('OK. Maybe another time') # message if game never started


    def start_game(self):
        welcome_msg = dedent('''\
        Welcome to Game of Greed
        (y)es to play or (n)o to decline''')
        print(welcome_msg)
        selection = input('> ')
        starting = selection.lower() == 'y'
        if starting:
            print(f'Starting round 1')
        return starting
    
    def exit_game(self):
        print(f'Thanks for playing. You earned {self.banker.balance} points')
        #reset game settings
        self.banker.clear_shelf()
        self.banker.balance = 0
        self.round = 1
        self.num_dice = 6
        sys.exit()

    def roll_dice(self, roller):
        print(f'Rolling {self.num_dice} dice...')
        return roller(self.num_dice)
       
    def print_roll(self, roll):
        roll_str = ''
        for die in roll:
            roll_str += str(die) + ' '
        print(f'*** {roll_str}***')
        
    def choose_and_validate_keepers(self, roll):
        validating, selection = True, ''
        while validating: #loop will continue until selection is validated
            self.print_roll(roll)
            if len(GameLogic.get_scorers(roll)) == 0:
                return 'ZILCH'
            print('Enter dice to keep, or (q)uit:')
            selection = input('> ')
            if selection.lower() == 'q':
                self.exit_game()
            selection = selection.replace(' ','') #remove whitespace
            #TODO Add regex to strip all values that aren't numbers
            keepers = tuple(map(int, list(selection)))
            if GameLogic.validate_keepers(roll, keepers):
                validating = False
            else:
                print('Cheater!!! Or possibly made a typo...')
        return selection

    def shelf_points(self, keepers):
        keepers = keepers.replace(' ', '') #remove whitespace
        dice = tuple(map(int, list(keepers))) # Adapted from https://www.geeksforgeeks.org/python-convert-string-to-tuple/
        score = GameLogic.calculate_score(dice)
        self.banker.shelf(score)
        self.num_dice -= len(dice)
        print(f'You have {self.banker.shelved} unbanked points and {self.num_dice} dice remaining')
        print('(r)oll again, (b)ank your points or (q)uit:')


    def end_round(self, banking = False):
        if not banking:
            self.banker.clear_shelf()
        print(f'You banked {self.banker.shelved} points in round {self.round}')
        if banking:
            self.banker.bank()
        self.banker.clear_shelf()
        print(f'Total score is {self.banker.balance} points')
        self.round += 1
        self.num_dice = 6
        print(f'Starting round {self.round}')
    
    def print_zilch_msg(self):
        zilch_msg = dedent('''\
        ****************************************
        **        Zilch!!! Round over         **
        ****************************************''')
        print(zilch_msg)


if __name__ == '__main__':
    game = None
    try:
        game = Game()
        game.play()
    except KeyboardInterrupt:
        game.exit_game()

        
   
        