#!/usr/bin/env python3
"""
Chinese Liar's Dice
You can learn more about the game here:
http://www.hushchina.com/chinese-dice-games/

Somtimes referred to as Chinese Bullshit
"""

class ChineseLiarsDice:
    """Helps calculate whether or not to call bullshit on a given prediction.

    Args:
        num_players (str): 

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """
    NUM_DICE = 24
    NUM_VALUES = 6
    NORMAL_PROBABILITY = 2 / NUM_VALUES
    VEGAN_PROBABILITY = 1 / NUM_VALUES
    WILDCARD_KEY = 'wildcard'

    def __init__(self, num_players):
        self.num_players = num_players
        self.num_dice_per_player = ChineseLiarsDice.NUM_DICE / num_players
        self.probability = ChineseLiarsDice.NORMAL_PROBABILITY
        self.num_other_die = ChineseLiarsDice.NUM_DICE

        # Set all known dice amounts to 0.
        count = {}
        for num in range(1, ChineseLiarsDice.NUM_VALUES + 1):
            count[num] = 0
        
        # Add the wildcard counter.
        count[ChineseLiarsDice.WILDCARD_KEY] = 0
        
        self.count = count

    def set_hand(self, hand):
        """
        Sets the player's hand to factor in known die into the probability.
        
        Args:
            hand (list(int)): The dice values. e.g. [1, 1, 3, 4]
        """
        for num in hand:
            self.count[num] += 1
        
        # 1's are wildcards.
        self.count[ChineseLiarsDice.WILDCARD_KEY] = self.count[1]

        # The number of unknown die decreases.
        self.num_other_die -= len(hand)

    def call_bullshit(self, num_dice, dice_value, vegan=False):
        """
        Decides whether or not to call bullshit on a given prediction by
        calculating the expected number of that die and checking if that is
        less than the given prediction.

        Args:
            num_dice (int): The number of dice that is predicted.
            dice_value (int): The value of the dice chosen.
        
        Returns:
            bool: True if you should call bullshit, False otherwise.
        """
        # When vegan is initiated all die probabilities are halved from 1/3 to
        # 1/6.
        if vegan or dice_value is 1:
            self.probability = ChineseLiarsDice.VEGAN_PROBABILITY
            self.count[ChineseLiarsDice.WILDCARD_KEY] = 0
        
        # The expected number of other people's die.
        num_predicted = self.probability * self.num_other_die

        # The number of our die.
        num_predicted += self.count[dice_value]

        # We add the wildcards. This is 0 when the round becomes vegan.
        num_predicted += self.count[ChineseLiarsDice.WILDCARD_KEY]

        if num_predicted < num_dice:
            return True
        
        return False

def main(args):
    CB = ChineseLiarsDice(6)
    hand = [1, 1, 1, 1]
    CB.set_hand(hand)
    num_dice = 10
    dice_value = 6
    vegan = False
    call = CB.call_bullshit(num_dice, dice_value, vegan=vegan)
    message = None
    if call:
        message = "You should call!"
    else:
        message = "You should NOT call!"
    print(message)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-d', '--debug',
                        help="Whether or not to run in debug mode.",
                        default=False,
                        action='store_true')

    args = parser.parse_args()
    main(args)