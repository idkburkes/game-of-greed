import random
from collections import Counter

class GameLogic:
    
    @staticmethod
    def roll_dice(num):
        rolls = []
        for _ in range(num):
            rolls.append(random.randint(1,6))
        return tuple(rolls)

    @staticmethod
    def calculate_score(dice):
        score = 0
        counter = Counter(dice)
        n = len(counter)
        if n == 6 and all(count == 1 for count in counter.values()):
            return 1500 #handle straight
        elif n == 3 and all(count == 2 for count in counter.values()):
            return 1500 #handle three pairs
        else:
            for num, count in counter.items(): 
                if count >= 3:
                    #handle 3-6 of a kind
                    score += GameLogic.calc_triples_and_above(num, count)
                else:
                    #handle single 1's and 5's 
                    score += GameLogic.calc_singles(num, count) 
        return score

    @staticmethod    
    def get_scorers(dice):
        '''
        Finds dice which are not worth points in the current hand and removes them from being calculated for points.
        Input: dice as a tuple
        Output: ret_dice as a tuple
        '''
        ret_dice = []
        counter = Counter(dice)
        n = len(counter)

        #If dice make a straight, just return them all
        #Example: {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
        #len = 6, and all counts == 1
        if n == 6 and all(count == 1 for count in counter.values()):
            return tuple(dice)
        #If dice make 3 pairs, just return them all
        #Example: {1: 2, 2: 2, 3: 2}
        #len = 3, and all counts == 2
        elif n == 3 and all(count == 2 for count in counter.values()):
            return tuple(dice)
        
        else:
            for num, count in counter.items():
                #If any number makes 3 or more of a kind, append them to the list
                #Example: {2: 3, 3: 2, 4: 1}
                #Here, 2 is appended
                if count >= 3:
                    for x in range(count):
                        ret_dice.append(num)
                else:
                    #Finally, if any number is a 1 or 5, append them to the list
                    #Example: {1: 1, 2: 1, 3: 1, 4: 1, 5: 2}
                    #Here, 1 and two 5's are appended
                    if num == 1 or num == 5:
                        for x in range(count):
                            ret_dice.append(num)

        return tuple(ret_dice)
            
    @staticmethod
    def validate_keepers(dice, held_dice):
        dice_counter = Counter(dice)
        held_dice_counter = Counter(held_dice)
        dice_n = len(dice_counter)
        held_n = len(held_dice_counter)
        val = False

        for h_num, h_count in held_dice_counter.items():
            for d_num, d_count in dice_counter.items():
                if h_num == d_num and h_count == d_count:
                    val = True
                    break
                else:
                    val = False
        return val

    @staticmethod
    def calc_triples_and_above(num, count):
        if num == 1:
            return 1000 * (count-2)
        else:
            return (100*num) * (count-2)

    @staticmethod
    def calc_singles(num, count):
        score = 0
        if num == 1: 
            score += 100 * count
        elif num == 5:
            score += 50 * count
        return score
