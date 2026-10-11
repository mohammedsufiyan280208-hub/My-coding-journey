import random

choices = ["rock", "paper", "scissor"]

player_score = 0
computer_score = 0
round_number = 1

print("=" * 35)
print("   ROCK PAPER SCISSOR")
print("        BEST OF 5")
print("=" * 35)

while player_score < 3 and computer_score < 3:

    print(f"\n--- Round {round_number} ---")

    player = input("Choose rock, paper, or scissor: ").lower().strip()

    if player not in choices:
        print("Invalid choice! Try again.")
        continue

    computer = random.choice(choices)

    print(f"\nYou chose: {player}")
    print(f"Computer chose: {computer}")

    if player == computer:
        print("Result: Draw!")

    elif (
        (player == "rock" and computer == "scissor")
        or (player == "paper" and computer == "rock")
        or (player == "scissor" and computer == "paper")
    ):
        print("Result: You win this round!")
        player_score += 1

    else:
        print("Result: Computer wins this round!")
        computer_score += 1

    print("\nSCOREBOARD")
    print(f"You: {player_score} | Computer: {computer_score}")

    round_number += 1

print("\n" + "=" * 35)

if player_score == 3:
    print("🏆 CONGRATULATIONS! YOU WON THE GAME!")
else:
    print("💻 COMPUTER WON THE GAME!")

print(f"Final Score: You {player_score} - {computer_score} Computer")
print("=" * 35)