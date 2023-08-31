"""
See "README.md" for information about the progress
"""

import random

suits = ["C", "D", "H", "S"]
values = list(range(2,11)) + ["J", "Q", "K", "A"]

deck = []


# One regular deck of playing cards (no jokers)
for s in suits:
    for v in values:
        if v in ["J", "Q", "K"]:
            deck.append(10)
        elif v == "A":
            deck.append(11)
        else:
            deck.append(v)
        

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
print("------------------------")

card = drawCard()
print(f"Your first card is {card}.")
player.append(card)

card = drawCard()
print(f"Your second card is {card}.")
player.append(card)


print(f"Your sum is now {sum(player)}.")

print()

# Dealer cards
dealer = []

# First card (hidden)
card = drawCard()
dealer.append(card)

# Second card (public)
card = drawCard()
dealer.append(card)
print(f"Dealers face up card is {card}.")


playing = True
won = True
bust = False

while playing:
    print()
    choice = input("Do you want to hit (h) or stand (s)? ")
    choice = choice.lower()
    
    if choice == "h":
        card = drawCard()
        print(f"Your next card is {card}.")
        player.append(card)
        print(f"Your sum is now {sum(player)}.")
        
    if choice == "s":
        print("You do not receive any more cards.")
        playing = False
        
    if sum(player) > 21:
        print("You bust!")
        playing = False
        won = False
        bust = True


if not bust:
    print()
    print("Dealers turn")
    print("------------------")

    print(f"Dealers first card: {dealer[0]}")
    print(f"Dealers second card: {dealer[1]}")
    print(f"Dealers total: {sum(dealer)}")

    while sum(dealer) <= 16:
        print()
        print("Dealer draws another card")
        card = drawCard()
        print(f"Dealer draws a {dealer[0]}")
        dealer.append(card)
        print(f"Dealers total: {sum(dealer)}")
        
    if sum(dealer) > 21:
        print("Dealer busts!")
        dealer = []
    else:
        print("Dealer stands.")
        
    print()
    
    print("You  | Dealer")
    print("--------------")
    print(f" {sum(player)}  |  {sum(dealer)}")
    
    print()
    
    if sum(player) > sum(dealer):
        print("You win!!!")
    elif sum(player) < sum(dealer):
        print("Dealer wins.")
    else:
        print("You and the dealer have the same hand-total (push)")

