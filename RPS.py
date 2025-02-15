import random


def quincy2(counter=[0]):

    counter[0] += 1
    choices = ["R", "R", "P", "P", "S"]
    return choices[counter[0] % len(choices)]



def mrugesh2(prev_opponent_play, opponent_history=[]):
    opponent_history.append(prev_opponent_play)
    last_ten = opponent_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)

    if most_frequent == '':
        most_frequent = "S"

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[most_frequent]


def kris2(prev_opponent_play):
    if prev_opponent_play == '':
        prev_opponent_play = "R"
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prev_opponent_play]



def abbey2(prev_opponent_play,
          opponent_history=[],
          play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]):
    

    if not prev_opponent_play:
        prev_opponent_play = 'R'
    #opponent_history.append(prev_opponent_play)




    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[last_two] += 1

    potential_plays = [
        prev_opponent_play + "R",
        prev_opponent_play + "P",
        prev_opponent_play + "S",
    ]

    sub_order = {
        k: play_order[k]
        for k in potential_plays if k in play_order
    }

    print(last_two)
    print(opponent_history)
    print(play_order)

    if last_two.count < 2:
        return 'P'
    
    prediction = max(sub_order, key=sub_order.get)[-1:]

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]



# Dynamic Strategy Based on Bot Classification
"""
Store the history of the player's moves and update the opponent's (bot) move history.
Simulate bot's behavior and compare it with player's behavior.

Args:
    prev_play (str): The move made by the opponent in the previous round.
    player_history (list): A list storing the player's previous moves.
    opponent_history (list): A list storing the opponent's (bot) previous moves.
    bot_history (dict): A dictionary storing bot histories (Quincy, Mrugesh, Kris, Abbey).
    bot_scores (dict): A dictionary storing accuracy scores of bots.
Returns:
    str: The move for the current round.
"""
def player(prev_play, player_history=[], opponent_history=[], bot_history={}, bot_scores={"quincy": 0, "mrugesh": 0, "kris": 0, "abbey": 0}):
    # Update opponent history with current move
    if prev_play:  # Ignore empty moves on first round
        opponent_history.append(prev_play)
    else:
        del player_history[:]
        del opponent_history[:]
        bot_history.clear()
        bot_scores={"quincy": 0, "mrugesh": 0, "kris": 0, "abbey": 0}
    
    # Simulate each bot's move based on the last player's move
    bots = {
        "quincy": quincy2,
        "mrugesh": mrugesh2,
        "kris": kris2,
        "abbey": abbey2,
    }
    
    bot_moves = {}
    canIden = False
    for bot_name, bot_func in bots.items():
        # If player_history is empty, use a default move ("R")
        last_player_move = player_history[-1] if player_history else "R"
        # Use the bot's strategy to calculate the next move based on the player's history
        if bot_name == "quincy":
            bot_moves[bot_name] = bot_func()  # Quincy will just return a sequence 
        elif bot_name == "abbey":
            bot_moves[bot_name] = bot_func(last_player_move,opponent_history=player_history) 
        else:
            bot_moves[bot_name] = bot_func(last_player_move)  # Other bots use player history

        # Store the bot's move in the bot_history for tracking purposes
        if bot_name not in bot_history:
            bot_history[bot_name] = []

        bot_history[bot_name].append(bot_moves[bot_name])


        # Compare lastest bot history with actual opponent move and increase score if same
        if prev_play and  bot_history[bot_name][-2] == prev_play:
            canIden = True
            if bot_scores[bot_name] + 1 >=3:
                bot_scores[bot_name] = 3
            else:
                bot_scores[bot_name] += 1
        else:
            bot_scores[bot_name] = bot_scores[bot_name]*0.7

    # Identify the most likely bot based on highest score
    best_bot = max(bot_scores, key=bot_scores.get)

    
    print("-----------------------")
    print(best_bot)
    # print("prev_play:" + prev_play)
    # print(bot_history)
    print(bot_scores)
    print("last player Move:" + last_player_move) 
 
    counter_moves = {"R": "P", "P": "S", "S": "R"}
    player_play = counter_moves[bot_history[best_bot][-1]]
    player_history.append(player_play)    
    return player_play