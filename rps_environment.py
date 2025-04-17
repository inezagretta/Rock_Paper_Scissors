class RPSEnvironment:
   """
   A class representing the Rock-Paper-Scissors environment where the game takes place.
   This environment handles the state, agent's action, opponent's action, and determines rewards.
   """
   def __init__(self):
       """
       Initialize the RPS environment.


       Attributes:
       - actions: A list of valid actions ('rock', 'paper', 'scissors').
       - state: The current state of the environment, which is the last move of the opponent.
       """
       self.actions = ['rock', 'paper', 'scissors']  # Possible actions in the game
       self.state = None  # Initial state is undefined


   def get_state(self):
       """
       Retrieve the current state of the environment.


       :return: The current state (last move of the opponent).
       """
       return self.state


   def step(self, agent_action, opponent_action):
       """
       Process a step in the environment by taking the agent's and opponent's actions.


       :param agent_action: The action chosen by the agent ('rock', 'paper', or 'scissors').
       :param opponent_action: The action chosen by the opponent.
       :return: A reward based on the outcome:
                0 for a tie,
                1 for a win,
               -1 for a loss.
       """
       # Update the environment's state to reflect the opponent's last action
       self.state = opponent_action

       # Determine the result of the game round
       if agent_action == opponent_action:
           return 0  # Tie, no reward or penalty
       elif (agent_action == 'rock' and opponent_action == 'scissors') or \
               (agent_action == 'paper' and opponent_action == 'rock') or \
               (agent_action == 'scissors' and opponent_action == 'paper'):
           return 1  # Agent wins, reward +1
       else:
           return -1  # Opponent wins, penalty -1
