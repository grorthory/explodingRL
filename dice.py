import random

class Dice:
    def __init__(self, starting_index):
        self.chain = [2, 4, 6, 8, 10, 12, 20]
        self.index = starting_index

    def roll(self):
        sides = self.chain[self.index]
        result = random.randint(1, sides)
        return result

    def upgrade(self):
        if self.index<len(self.chain)-1:
            self.index += 1

    def downgrade(self):
        if self.index > 0:
            self.index -= 1