import tkinter as tk # for GUI
from Game import RPSGame # game logic
if __name__ == "__main__":
   # Create the main Tkinter window
   root = tk.Tk()
   # Initialize the Rock-Paper-Scissors game
   game = RPSGame(root)
   # Start the Tkinter main event loop
   root.mainloop()
