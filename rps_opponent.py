import random
class RandomOpponent:
   """
   A class representing an opponent that chooses actions randomly.
   """
   def __init__(self, actions):
       """
       Initialize the RandomOpponent.


       :param actions: A list of possible actions (e.g., ["Rock", "Paper", "Scissors"]).
       """
       self.actions = actions  # List of possible actions


   def choose_action(self):
       """
       Randomly select an action from the available actions.


       :return: A randomly chosen action.
       """
       return random.choice(self.actions)  # Selects a random action




class PatternedOpponent:
   """
   A class representing an opponent that follows a predefined pattern of actions.
   """
   def __init__(self, actions, pattern):
       """
       Initialize the PatternedOpponent.


       :param actions: A list of possible actions (e.g., ["Rock", "Paper", "Scissors"]).
       :param pattern: A list defining the sequence of actions the opponent will follow.
       """
       self.actions = actions  # List of possible actions
       self.pattern = pattern  # Predefined sequence of actions
       self.index = 0  # Index to track the current position in the pattern


   def choose_action(self):
       """
       Select the next action based on the predefined pattern.


       :return: The action from the pattern at the current index with 90% probability.
       """
       if random.random() < 0.9:
           action = self.pattern[self.index]  # Get the current action in the pattern
       else:
           action = random.choice(self.actions)  # Selects a random action


       self.index = (self.index + 1) % len(self.pattern)  # Move to the next action in a circular manner
       return action
