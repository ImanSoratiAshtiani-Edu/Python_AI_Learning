import random

# function create a card
def create():
    card = cards.pop(random.randint(0,len(cards)-1))
    try:
        card=int(card)
    except:
        card=11 if card == 'A' else 10
    return card
# function computer
def computer_cards_prep():
    global computer_state
    while sum(computer_list) < 17:
        computer_list.append(create())
    computer_state = check(computer_list)
# function player
def player_card_prep():
    global player_state
    while True:
        print(f'Your cards: {player_list}, current score: {sum(player_list)}')
        print("computer's first card:", computer_list[0])
        player_state = check(player_list)
        if player_state == 0 or player_state >= 21: break
        if input("Type 'y' to get another card, type 'n' to pass: ").lower() == 'y':
            player_list.append(create())
        else:
            break
# function check
def check(l):
    if sum(l) > 21:
        if l.count(11):
            l[l.index(11)]=1
            state = check(l)
        else:
            state= 0
    elif sum(l) == 21:
        if len(l)==2:
            state=22 #BJ
        else:
            state = sum(l) # 21
    else:
        state = sum(l) # <21
    return state

# compare
def compare():
    print(f'Your final hand: {player_list}, final score: {sum(player_list)}')
    print(f"Computer's final hand: {computer_list}, final score: {sum(computer_list)}")
    if player_state < computer_state:
        result='You lose 😒'
    elif player_state > computer_state:
            result='You won 😁'
    else:   # state is equal
        if player_state==0:
            result='You went over. You lose 😫'
        else:
            result = 'Draw 🥴'
    return result
# operations:
# list of cards
while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower() == 'y':
    cards=[2,3,4,5,6,7,8,9,10,'J','Q','K','A']
    print(cards)
    player_list=list()
    computer_list=list()
    computer_state=None
    player_state=None
    for i in range(2):
        player_list.append(create())
        computer_list.append(create())
    computer_cards_prep()
    player_card_prep()
    print(compare())




