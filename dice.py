import random

class Dice:
    def __init__(self, starting_index):
        self.chain = [2, 4, 6, 8, 10, 12, 20]
        self.index = starting_index

    def flatroll(self):
        sides = self.chain[self.index]
        result = random.randint(1, sides)
        return result

    def luckyroll(self, luck_points, overkill_threshold=None):
                total_sum = 0
                current_index = self.index
                remaining_luck = luck_points
                luck_spent_this_sequence = 0
                roll_history = []

                while True:
                    sides = self.chain[current_index]
                    roll = random.randint(1, sides)

                    forced_explosion = False

                    # Logic for spending luck:
                    # 1. Roll didn't explode naturally (roll < sides)
                    # 2. Difference to explode is exactly 1 (sides - roll == 1)
                    # 3. Haven't spent luck yet this sequence (luck_spent_this_sequence == 0)
                    # 4. Player has at least 1 luck point (remaining_luck >= 1)
                    # 5. Not overkill: Only spend if current total_sum + roll is LESS than threshold
                    if roll < sides and (sides - roll == 1) and luck_spent_this_sequence == 0 and remaining_luck >= 1:
                        # If we don't have a threshold, or if we do and we haven't reached it yet
                        if overkill_threshold is None or (total_sum + roll < overkill_threshold):
                            remaining_luck -= 1
                            luck_spent_this_sequence = 1
                            roll = sides  # Force max value to trigger explosion
                            forced_explosion = True

                    total_sum += roll

                    # Formatting for the message log
                    if roll == sides:
                        tag = "!*" if forced_explosion else "!"
                        roll_history.append(f"{roll}{tag}")
                        # Move up the chain if possible, otherwise stay at max
                        if current_index < len(self.chain) - 1:
                            current_index += 1
                        continue  # Explode!
                    else:
                        roll_history.append(str(roll))
                        break

                return total_sum, remaining_luck, roll_history

    def upgrade(self):
        if self.index<len(self.chain)-1:
            self.index += 1

    def downgrade(self):
        if self.index > 0:
            self.index -= 1