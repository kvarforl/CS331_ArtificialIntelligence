'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
from OthelloBoard import OthelloBoard #imported for static type checking

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
       
    def get_move(self, board):
        return self._minimax_decision(board)
    
    def _minimax_decision(self, state: OthelloBoard):
        actions = list(state.get_legal_moves(self.symbol))
        value = float("-inf")
        for a in actions:
            clone = state.cloneOBoard() #preserve initial board
            clone.play_move(a[0], a[1], self.symbol) #generate successor
            if(self._min_value(clone) > value): #choose action with max value
                champ_action = a
        return champ_action
    
    #assign value to terminal state( positive for symb win, - for oppsym win)  
    def _utility(self, state: OthelloBoard):
        xscore = state.count_score(self.symbol)
        oscore = state.count_score(self.oppSym)
        return xscore - oscore

    #state is an othello board object
    #maximizing player
    def _max_value(self, state: OthelloBoard):
        if not(state.has_legal_moves_remaining(self.symbol)):
            return self._utility(state)
        value = float('-inf')
        actions = list(state.get_legal_moves(self.symbol))
        for a in actions:
            clone = state.cloneOBoard() #preserve initial board
            clone.play_move(a[0], a[1], self.symbol) #generate successor
            value = max(value, self._min_value(clone))
        return value

    #state is an othello board object
    #minimizing player
    def _min_value(self, state: OthelloBoard):
        if not(state.has_legal_moves_remaining(self.oppSym)):
            return self._utility(state)
        value = float('inf')
        actions = list(state.get_legal_moves(self.oppSym))
        for a in actions:
            clone = state.cloneOBoard() #preserve initial board
            clone.play_move(a[0], a[1], self.oppSym) #generate successor
            value = min(value, self._max_value(clone))
        return value

                    





