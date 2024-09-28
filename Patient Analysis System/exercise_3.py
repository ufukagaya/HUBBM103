import random

target = random.randint(1, 25)
N = int(input("Guess a number between 1 and 25\nPlease enter a number: "))

running = True
while running:
    if N < target:
        N = int(input("Increase your number: "))
    elif N > target:
        N = int(input("Decrease your number: "))
    else:
        running = False

print("You won!")