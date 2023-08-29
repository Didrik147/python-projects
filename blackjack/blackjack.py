"""
TODO
- [ ] Variable value for ace (11 or 1)
- [ ] Add dealer
- [ ] Add money
- [ ] Add graphics (pygame?)
- [ ] Other rules?
"""

import random

suits = ["C", "D", "H", "S"]

deck = []

# One regular deck of playing cards (no jokers)
for s in suits:
    for i in range(1, 13+1):
        if i > 10:
            i = 10
        deck.append(i)
        

# Shuffle the deck
random.shuffle(deck)

# Draw a random card
def drawCard():
    global deck
    i = random.randint(1, len(deck)-1)
    card = deck[i]

    # Removes the card from the deck
    deck.pop(i)

    return card


# Player cards
player = []

print("Welcome to blackjack!")
card = drawCard()
print(f"Your first card is {card}.")
player.append(card)

card = drawCard()
print(f"Your second card is {card}.")
player.append(card)

total = sum(player)

print(f"Your sum is now {total}.")

playing = True

while playing:
    print()
    choice = input("Do you want to hit (h) or stand (s)? ")
    choice = choice.lower()
    
    if choice == "h":
        card = drawCard()
        print(f"Your next card is {card}.")
        player.append(card)
        total = sum(player)
        print(f"Your sum is now {total}.")
        
    if choice == "s":
        print("You do not receive any more cards.")
        playing = False
        
    if total > 21:
        print("You bust!")
        playing = False



