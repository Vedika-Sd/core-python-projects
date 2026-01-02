import random

CHOICES = {'r': 'Rock', 'p': 'Paper', 's': 'Scissors'} # Store choices with their full names in dictionary

# WIN_RULES maps a choice to the choice it defeats, e.g. 'r' beats 's'
WIN_RULES = {'r': 's', 'p': 'r', 's': 'p'}


class RockPaperScissors:
    """Simple Rock-Paper-Scissors game implemented with OOP principles.

    - Keeps a running score
    - Validates input (accepts 'r', 'p', 's' and full words)
    - Can play multiple rounds until the user quits
    """

    def __init__(self):       
        self.score = {'user': 0, 'computer': 0, 'ties': 0}

    def _normalize(self, choice: str):
        if not choice:
            return None
        c = choice.strip().lower()
        synonyms = {'rock': 'r', 'paper': 'p', 'scissors': 's', 'scissor': 's'}
        if c in synonyms:
            return synonyms[c]
        if c in CHOICES:
            return c
        return None

    def get_computer_choice(self):
        return random.choice(list(CHOICES.keys()))

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return 'tie'
        
        # If the choice that user_choice defeats equals computer_choice, user wins
        if WIN_RULES[user_choice] == computer_choice:
            return 'user'
        else:
            return 'computer'

    def play_round(self):
        while True:
            raw = input("Enter your choice (r=rock, p=paper, s=scissors) or 'q' to quit: ")
            if raw.strip().lower() == 'q':
                return None
            user = self._normalize(raw)
            if user is None:
                print("Invalid choice. Please enter r, p, s, rock, paper, or scissors.")
                continue

            comp = self.get_computer_choice()
            winner = self.determine_winner(user, comp)

            if winner == 'tie':
                self.score['ties'] += 1
                print(f"Both chose {CHOICES[user]}. It's a tie.")
            elif winner == 'user':
                self.score['user'] += 1
                print(f"You win! {CHOICES[user]} beats {CHOICES[comp]}.")
            else:
                self.score['computer'] += 1
                print(f"You lose. {CHOICES[comp]} beats {CHOICES[user]}.")

            print(f"Computer chose: {CHOICES[comp]} ({comp}) and you chose: {CHOICES[user]} ({user})")
            print(f"Score -> You: {self.score['user']} Computer: {self.score['computer']} Ties: {self.score['ties']}")
            return True

    def play(self):
        print("Welcome to Rock Paper Scissors Game")
        while True:
            result = self.play_round()
            if result is None:
                print("Thanks for playing! Final score:")
                print(f"You: {self.score['user']} Computer: {self.score['computer']} Ties: {self.score['ties']}")
                break


if __name__ == '__main__':
    game = RockPaperScissors()
    game.play()