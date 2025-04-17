import random
class QLearningAgent:
   def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
       """
       Initialize the Q-learning agent.


       :param actions: A list of possible actions the agent can take (e.g., ["Rock", "Paper", "Scissors"]).
       :param learning_rate: The rate at which the agent updates its Q-values (alpha).
       :param discount_factor: The factor for future rewards (gamma).
       :param epsilon: The probability of choosing a random action (exploration rate).
       """
       self.actions = actions  # List of possible actions
       self.learning_rate = learning_rate  # Learning rate for Q-value updates
       self.discount_factor = discount_factor  # Discount factor for future rewards
       self.epsilon = epsilon  # Exploration rate for epsilon-greedy policy
       self.q_table = {}  # Dictionary to store Q-values, indexed by (state, action) pairs


   def get_q_value(self, state, action):
       """
       Retrieve the Q-value for a given state-action pair.


       :param state: The current state.
       :param action: The action taken in the current state.
       :return: The Q-value associated with the state-action pair, defaulting to 0.0 if not found.
       """
       return self.q_table.get((state, action), 0.0)


   def choose_action(self, state):
       """
       Choose an action using an epsilon-greedy policy.


       With probability epsilon, choose a random action (exploration).
       Otherwise, choose the action with the highest Q-value (exploitation).


       :param state: The current state.
       :return: The chosen action.
       """
       if random.random() < self.epsilon:
           # Explore: Randomly select an action
           return random.choice(self.actions)
       else:
           # Exploit: Choose the action with the highest Q-value
           q_values = [self.get_q_value(state, a) for a in self.actions]
           max_q = max(q_values)  # Maximum Q-value
           # Find all actions with the maximum Q-value (in case of ties)
           best_actions = [i for i in range(len(self.actions)) if q_values[i] == max_q]
           # Randomly select among the best actions to break ties
           return self.actions[random.choice(best_actions)]


   def learn(self, state, action, reward, next_state):
       """
       Update the Q-value for the given state-action pair using the Q-learning formula.


       Q(s, a) <- Q(s, a) + alpha * [reward + gamma * max(Q(s', a')) - Q(s, a)]


       :param state: The current state.
       :param action: The action taken.
       :param reward: The reward received after taking the action.
       :param next_state: The next state resulting from the action.
       """
       current_q = self.get_q_value(state, action)  # Current Q-value for (state, action)
       # Calculate the maximum Q-value for the next state
       max_next_q = max([self.get_q_value(next_state, a) for a in self.actions])
       # Update the Q-value using the Q-learning update rule
       new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
       # Store the updated Q-value in the Q-table
       self.q_table[(state, action)] = new_q
