from OthelloBoard import OthelloBoard #imported for static type checking

def minimax_decision(state: OthelloBoard):
    actions = list(state.get_legal_moves("O"))
    value = float("-inf")
    for a in actions:
        clone = state.cloneOBoard() #preserve initial board
        clone.play_move(a[0], a[1], "O") #generate successor
        if(min_value(clone) > value): #choose action with max value
            champ_action = a
    return champ_action
 
 #assign value to terminal state( positive for X win, - for 0 win)  
def utility(state: OthelloBoard):
    xscore = state.count_score("X")
    oscore = state.count_score("O")
    return xscore - oscore

#state is a Board object
#p1 is always X, maximizing player
def max_value(state: OthelloBoard):
    if not(state.has_legal_moves_remaining("X")):
        return utility(state)
    value = float('-inf')
    actions = list(state.get_legal_moves("X"))
    for a in actions:
        clone = state.cloneOBoard() #preserve initial board
        clone.play_move(a[0], a[1], "X") #generate successor
        value = max(value, min_value(clone))
    return value

#state is a Board object
#p2 is always O, minimizing player
def min_value(state: OthelloBoard):
    if not(state.has_legal_moves_remaining("O")):
        return utility(state)
    value = float('inf')
    actions = list(state.get_legal_moves("O"))
    for a in actions:
        clone = state.cloneOBoard() #preserve initial board
        clone.play_move(a[0], a[1], "O") #generate successor
        value = min(value, max_value(clone))
    return value