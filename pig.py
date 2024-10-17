#Stephon Kumar
import random
import argparse

# This class represents a six-sided die that players will roll
class Die:
    def __init__(self):
        # Set a random seed for consistency in testing
        random.seed(0)
        self.value = 0

    # This method simulates rolling the die and returns a value between 1 and 6
    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

# This class represents a player in the Pig game
class Player:
    def __init__(self, name):
        self.name = name  # Player's name
        self.score = 0  # Player's total score in the game
        self.turn_total = 0  # Score accumulated during the current turn

    # Resets the score accumulated during the current turn
    def reset_turn_total(self):
        self.turn_total = 0

    # Adds points from a die roll to the player's current turn total
    def add_to_turn_total(self, value):
        self.turn_total += value

    # Ends the player's turn by adding the turn total to the total score
    def hold(self):
        self.score += self.turn_total
        self.reset_turn_total()  # Reset turn total after holding

    # Resets the player's total score (for starting a new game)
    def reset_score(self):
        self.score = 0

# This class controls the overall flow of the Pig game
class PigGame:
    def __init__(self, num_players):
        # Create a list of players based on the number of players specified
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.current_player = 0  # Index to keep track of whose turn it is
        self.die = Die()  # A single die object shared among all players
        self.winner = None  # Track the winner once someone wins

    # Switch to the next player after the current player's turn ends
    def switch_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    # Check if the current player has won by reaching a score of 100 or more
    def check_winner(self):
        if self.players[self.current_player].score >= 100:
            self.winner = self.players[self.current_player].name

    # This method handles the gameplay for each player's turn
    def play_turn(self):
        player = self.players[self.current_player]
        print(f"{player.name}'s turn!")  # Inform the user whose turn it is

        while True:
            # Display current turn's total and player's overall score
            print(f"Current turn total: {player.turn_total}, Current score: {player.score}")
            action = input("Enter 'r' to roll or 'h' to hold: ").lower()  # Get user input for the next action

            if action == 'r':
                # Roll the die and store the result
                roll_value = self.die.roll()
                print(f"Rolled: {roll_value}")

                if roll_value == 1:
                    # If a 1 is rolled, the player loses all points for this turn
                    print(f"{player.name} rolled a 1. Turn over with no points added.")
                    player.reset_turn_total()  # Reset the turn total
                    break  # End the turn
                else:
                    # Add the rolled value to the player's turn total
                    player.add_to_turn_total(roll_value)

            elif action == 'h':
                # The player chooses to hold, adding the turn total to their overall score
                player.hold()
                print(f"{player.name} holds. Total score: {player.score}")
                break  # End the turn after holding

            # After each roll or hold, check if the player has won
            self.check_winner()
            if self.winner:
                print(f"{self.winner} wins the game!")
                return  # End the game if there's a winner

        # If no one has won, switch to the next player
        self.switch_player()

    # This method starts and manages the game loop until there's a winner
    def play_game(self):
        print("Welcome to the Pig Game!")  # Greeting at the start of the game
        while not self.winner:
            # Keep playing until someone wins
            self.play_turn()

        # Game over, display scores
        print("Game over!")
        for player in self.players:
            print(f"{player.name}: {player.score}")

    # Resets the game to play again by resetting all scores and the winner
    def reset_game(self):
        self.winner = None  # Clear the winner
        for player in self.players:
            player.reset_score()  # Reset each player's score

# Main entry point for the program
if __name__ == "__main__":
    # Use argparse to handle command line arguments for the number of players
    parser = argparse.ArgumentParser(description="Play the Pig game.")
    parser.add_argument('--numPlayers', type=int, default=2, help="Number of players (default: 2)")
    args = parser.parse_args()

    # Initialize the game with the specified number of players
    game = PigGame(args.numPlayers)

    # Main game loop to allow multiple games
    while True:
        game.play_game()  # Start the game

        # Ask the user if they want to play another game
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break  # Exit the game loop if the user doesn't want to play again

        # Reset the game for the next round
        game.reset_game()
        print("\nStarting a new game...\n")
