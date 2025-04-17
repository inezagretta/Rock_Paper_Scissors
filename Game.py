import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from rps_opponent import RandomOpponent, PatternedOpponent
from q_learning_agent import QLearningAgent
from rps_environment import RPSEnvironment




class RPSGame:
   """
   A class to implement the Rock-Paper-Scissors game with Q-learning. It provides a GUI interface and allows
   users to play against different types of opponents while tracking performance metrics.
   """


   def __init__(self, master):
       """
       Initialize the game environment and GUI components.


       :param master: The root Tkinter window.
       """
       self.master = master
       self.master.title("Rock Paper Scissors Q-Learning")
       self.env = RPSEnvironment()  # The game environment
       self.agent = None  # Q-learning agent
       self.opponent = None  # Opponent (can be random, patterned, or human)
       self.human_choice = tk.StringVar()  # Tracks the human's choice during the game
       self.game_in_progress = False  # Indicates whether a game is active
       self.create_widgets()  # Setup GUI widgets


   def create_widgets(self):
       """
       Create and organize the GUI components for the game.
       """
       # Opponent selection frame
       self.opponent_frame = ttk.Frame(self.master)
       self.opponent_frame.pack(pady=10)


       ttk.Label(self.opponent_frame, text="Choose your opponent:").pack(side=tk.LEFT, padx=5)
       ttk.Button(self.opponent_frame, text="Random", command=lambda: self.start_game("Random")).pack(side=tk.LEFT,
                                                                                                      padx=5)
       ttk.Button(self.opponent_frame, text="Patterned", command=lambda: self.start_game("Patterned")).pack(
           side=tk.LEFT, padx=5)
       ttk.Button(self.opponent_frame, text="Human", command=lambda: self.start_game("Human")).pack(side=tk.LEFT,
                                                                                                    padx=5)


       # Human choice buttons
       self.human_choice_frame = ttk.Frame(self.master)
       self.human_choice_frame.pack(pady=10)


       ttk.Button(self.human_choice_frame, text="Rock", command=lambda: self.make_human_choice("rock")).pack(
           side=tk.LEFT, padx=5)
       ttk.Button(self.human_choice_frame, text="Paper", command=lambda: self.make_human_choice("paper")).pack(
           side=tk.LEFT, padx=5)
       ttk.Button(self.human_choice_frame, text="Scissors", command=lambda: self.make_human_choice("scissors")).pack(
           side=tk.LEFT, padx=5)


       # Text area to display results
       self.result_text = tk.Text(self.master, height=20, width=50)
       self.result_text.pack(pady=10)


       # Plot for metrics
       self.fig, self.ax = plt.subplots(figsize=(5, 3))
       self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
       self.canvas.get_tk_widget().pack()


   def start_game(self, opponent_type):
       """
       Initialize the game with the selected opponent type and start the gameplay.


       :param opponent_type: The type of opponent ("Random", "Patterned", or "Human").
       """
       self.result_text.delete(1.0, tk.END)  # Clear previous results
       self.agent = QLearningAgent(self.env.actions)  # Initialize the Q-learning agent


       if opponent_type == "Random":
           self.opponent = RandomOpponent(self.env.actions)
           self.play_game(10000)  # Play 10,000 rounds with the random opponent
       elif opponent_type == "Patterned":
           self.opponent = PatternedOpponent(self.env.actions, ['rock', 'paper', 'scissors', 'rock', 'rock'])
           self.play_game(10000)  # Play 10,000 rounds with the patterned opponent
       elif opponent_type == "Human":
           self.result_text.insert(tk.END, "Click Rock, Paper or Scissors above!\n")
           self.human_play(100)  # Play 10 rounds with the human opponent


   def play_game(self, num_episodes):
       """
       Automate the game with the selected opponent for multiple episodes.


       :param num_episodes: The number of episodes to play.
       """
       total_reward = 0
       wins, losses, ties = 0, 0, 0  # Track metrics
       rewards_over_time = []


       for episode in range(num_episodes):
           state = self.env.get_state()
           agent_action = self.agent.choose_action(state)
           opponent_action = self.opponent.choose_action()
           reward = self.env.step(agent_action, opponent_action)
           next_state = self.env.get_state()
           self.agent.learn(state, agent_action, reward, next_state)


           total_reward += reward
           if reward == 1:
               wins += 1
           elif reward == -1:
               losses += 1
           else:
               ties += 1


           rewards_over_time.append(total_reward / (episode + 1))  # Track average reward


           if episode % 100 == 0 or episode == num_episodes - 1:
               self.update_metrics(total_reward, wins, losses, ties, episode + 1)


       self.plot_results(rewards_over_time, "Average Reward Over Time")


   def human_play(self, num_games):
       """
       Allow a human player to play against the Q-learning agent.


       :param num_games: The number of games to play.
       """
       self.game_in_progress = True
       self.human_choice_frame.pack()


       total_reward = 0
       wins, losses, ties = 0, 0, 0  # Track metrics
       rewards_over_time = []


       for game in range(num_games):
           state = self.env.get_state()
           agent_action = self.agent.choose_action(state)


           self.result_text.insert(tk.END, f"Game {game + 1} - Make your choice\n")
           self.result_text.see(tk.END)


           self.master.wait_variable(self.human_choice)
           human_action = self.human_choice.get()
           self.human_choice.set("")


           reward = self.env.step(agent_action, human_action)
           next_state = self.env.get_state()
           self.agent.learn(state, agent_action, reward, next_state)


           total_reward += reward
           if reward == 1:
               wins += 1
               result = "Agent wins!"
           elif reward == -1:
               losses += 1
               result = "Human wins!"
           else:
               ties += 1
               result = "It's a tie!"


           rewards_over_time.append(total_reward / (game + 1))  # Track average reward


           self.update_metrics(total_reward, wins, losses, ties, game + 1)
           self.result_text.insert(tk.END, f"Agent chose: {agent_action}\n")
           self.result_text.insert(tk.END, f"{result}\n")
           self.result_text.insert(tk.END, "--------------------\n")
           self.result_text.see(tk.END)


       self.human_choice_frame.pack_forget()
       self.game_in_progress = False
       self.plot_results(rewards_over_time, "Average Reward Over Time (Human Play)")


   def make_human_choice(self, choice):
       """
       Set the human player's choice during gameplay.


       :param choice: The human player's selected action.
       """
       if self.game_in_progress:
           self.human_choice.set(choice)


   def update_metrics(self, total_reward, wins, losses, ties, num_games):
       """
       Update the game metrics and display them in the GUI.


       :param total_reward: The total reward accumulated so far.
       :param wins: The number of wins.
       :param losses: The number of losses.
       :param ties: The number of ties.
       :param num_games: The number of games played so far.
       """
       win_rate = wins / num_games
       average_reward = total_reward / num_games
       self.result_text.insert(tk.END, f"Win Rate: {win_rate:.2f}\n")
       self.result_text.insert(tk.END, f"Average Reward: {average_reward:.2f}\n")
       self.result_text.insert(tk.END, f"Wins: {wins}, Losses: {losses}, Ties: {ties}\n")
       self.result_text.see(tk.END)


   def plot_results(self, rewards_over_time, title):
       """
       Plot the average rewards over time on the GUI.


       :param rewards_over_time: List of average rewards at each step.
       :param title: The title for the plot.
       """
       self.ax.clear()
       self.ax.plot(rewards_over_time)
       self.ax.set_title(title)
       self.ax.set_xlabel("Episode")
       self.ax.set_ylabel("Average Reward")
       self.canvas.draw()