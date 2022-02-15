import random


class MyPlayer:
    """First cooperates, then plays the other players last move, except for weird cases"""
    def __init__(self, payoff_matrix, *number_of_iterations):
        self.punishment = ((payoff_matrix[1])[1])[0]  # when both players defect
        self.temptation = ((payoff_matrix[0])[1])[1]  # when this player defects, but the other one cooperates
        self.sucker = ((payoff_matrix[0])[1])[0]      # when this player cooperates, but the other one defects
        self.reward = ((payoff_matrix[0])[0])[0]      # when both players cooperate
        self.opponent_history = []                    # A list where we record opponent's moves
        self.iterations = number_of_iterations        # Number of iterations the game has

    def record_opponents_move(self, opponent_move):
        """Add an item to history based on opponent's last move"""
        if opponent_move:
            self.opponent_history += ["Defect"]
        else:
            self.opponent_history += ["Cooperate"]

    # simple static methods for better readability
    @staticmethod
    def defect():
        return True

    @staticmethod
    def likely_defect():  # For getting out infinite defect loop in case of noise
        probability = random.randint(1, 50)
        if probability == 1:
            return False
        else:
            return True

    @staticmethod
    def cooperate():
        return False

    @staticmethod
    def likely_cooperate():  # For getting out of infinite cooperate loop in case cooperate is the worse option \
        #  and there's noise
        probability = random.randint(1, 50)
        if probability == 1:
            return True
        else:
            return False

    @staticmethod
    def do_random():
        probability = random.randint(0, 1)
        if probability == 1:
            return True
        else:
            return False

    def move(self):
        if self.iterations == 1:  # If there is only one iteration, return the better option
            if self.temptation > self.reward and self.punishment > self.sucker:
                return self.defect()
            elif self.reward > self.temptation and self.sucker > self.punishment:
                return self.cooperate()
            elif self.temptation > self.reward and self.sucker > self.punishment:
                if (self.temptation - self.reward) > (self.sucker - self.punishment):
                    return self.defect()
                else:
                    return self.cooperate()
            else:
                if (self.reward - self.temptation) > (self.punishment - self.sucker):
                    return self.cooperate()
                else:
                    return self.defect()

        elif self.reward == 0 and self.punishment == 0 and len(self.opponent_history) > 1:
            # If both players doing the same thing yields no points and the opponent consistently chooses one
            # thing, either do the opposite of what he does to get points, or, if that yields no points either,
            # mimic his move to give him less points.
                if self.opponent_history[-1] == "Defect" and self.opponent_history[-2] == "Defect":
                    if self.sucker != 0:
                        return self.cooperate()
                    else:
                        return self.defect()

                elif self.opponent_history[-1] == "Cooperate" and self.opponent_history[-2] == "Cooperate":
                    if self.temptation != 0:
                        return self.defect()
                    else:
                        return self.cooperate()
                else:
                    return self.do_random()

        elif self.reward == self.punishment and self.temptation > self.reward < self.sucker and \
                len(self.opponent_history) > 1:
            # If both players doing the same thing yields the same points and the two options left yield more points,
            # try to do the opposite of what the opponent does
            if self.opponent_history[-1] == "Defect" and self.opponent_history[-2] == "Defect":
                return self.cooperate()
            elif self.opponent_history[-1] == "Defect":
                return self.cooperate()
            elif self.opponent_history[-1] == "Cooperate" and self.opponent_history[-2] == "Cooperate":
                return self.defect()
            elif self.opponent_history[-1] == "Cooperate":
                return self.defect()
            else:
                return self.do_random()

        elif self.reward == 0:  # if one option's payoff is zero, always do the other thing
            return self.defect()
        elif self.punishment == 0:
            return self.cooperate()

        elif self.reward > self.punishment:  # In the case of a "normal" payoff matrix
            # First cooperate, then mimic the other player's last move
            if not self.opponent_history:
                return self.cooperate()
            elif self.opponent_history[-1] == "Defect":
                return self.likely_defect()
            else:
                return self.cooperate()

        elif self.reward < self.punishment:  # if the payoffs are reversed, normal strategy but switch coop with defect
            # First defect, then mimic the other player's last move
            if not self.opponent_history:
                return self.defect()
            elif self.opponent_history[-1] == "Defect":
                return self.defect()
            else:
                return self.likely_cooperate()

        else:  # If there's something the algorithm doesn't address, return random option
            return self.do_random()
