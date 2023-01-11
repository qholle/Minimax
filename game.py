import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        drop_phase = True

        #check if drop phase is over
        pieces = 0
        for row in state:
            pieces += row.count('b') + row.count('r')
        if(pieces >= 8):
            drop_phase = False
        
        move = []

        #move phase
        if not drop_phase:
            succs = self.move_phase_succ(state, self.my_piece)
            alpha = float('-inf')
            beta = float('inf')
            next_move = [(0,0), (0,0)]
            for succ in succs:
                temp_state = copy.deepcopy(state)
                temp_state[succ[0][0]][succ[0][1]] = self.my_piece
                temp_state[succ[1][0]][succ[1][1]] = ' '
                succ_value = self.min_value(temp_state, 3, alpha, beta)
                if (alpha < succ_value):
                    alpha = succ_value
                    next_move = succ
            move = next_move
            print(move)
            return move

        #drop phase
        succs = self.drop_phase_succ(state)
        alpha = float('-inf')
        beta = float('inf')
        next_move = (0,0)
        for succ in succs:
            row = succ[0]
            col = succ[1]
            temp_state = copy.deepcopy(state)
            temp_state[row][col] = self.my_piece
            succ_value = self.min_value(temp_state, 3, alpha, beta)
            if (alpha < succ_value):
                alpha = succ_value
                next_move = (row, col)
        move.insert(0, next_move)
        print(move)
        return move

    def drop_phase_succ(self, state):
        succ = []
        #find all empty spaces on the board
        for row in range(5):
            for col in range(5):
                if state[row][col] == ' ':
                    succ.append((row, col))
        return succ

    def move_phase_succ(self, state, piece):
        succ = []
        for row in range(5):
            for col in range(5):
                if state[row][col] == piece:
                    #left of the piece
                    if row > 0 and state[row-1][col] == ' ':
                        succ.append([(row-1, col), (row, col)])
                    #right of the piece
                    if row < 4 and state[row+1][col] == ' ':
                        succ.append([(row+1, col), (row, col)])
                    #above the piece
                    if col > 0 and state[row][col-1] == ' ':
                        succ.append([(row, col-1), (row, col)])
                    #below the piece
                    if col < 4 and state[row][col+1] == ' ':
                        succ.append([(row, col+1), (row, col)])
                    #above and left of the piece
                    if row > 0 and col > 0 and state[row-1][col-1] == ' ':
                        succ.append([(row-1, col-1), (row, col)])
                    #above and right of the piece
                    if row > 0 and col < 4 and state[row-1][col+1] == ' ':
                        succ.append([(row-1, col+1), (row, col)])
                    #below and left of the piece
                    if row < 4 and col > 0 and state[row+1][col-1] == ' ':
                        succ.append([(row+1, col-1), (row, col)])
                    #below and right of the piece
                    if row < 4 and col < 4 and state[row+1][col+1] == ' ':
                        succ.append([(row+1, col+1), (row, col)])
        return succ

    def max_value(self, state, depth, alpha, beta):
        if (self.game_value(state) != 0):
            return self.game_value(state)
        elif depth == 0:
            return self.heuristic_game_value(state)
        else:
            pieces = 0
            for row in state:
                pieces += row.count('b') + row.count('r')
            if(pieces >= 8):
                #move phase
                succs = self.move_phase_succ(state, self.my_piece)
                for succ in succs:
                    temp_state = copy.deepcopy(state)
                    temp_state[succ[0][0]][succ[0][1]] = self.my_piece
                    temp_state[succ[1][0]][succ[1][1]] = ' '
                    #recursively call opposite function at a lower depth
                    alpha = max(alpha, self.min_value(state, depth-1, alpha, beta))
                    if (alpha >= beta):
                        return beta
                return alpha
            else:
                #drop phase
                succs = self.drop_phase_succ(state)
                for succ in succs:
                    temp_state = copy.deepcopy(state)
                    temp_state[succ[0]][succ[1]] = self.my_piece
                    #recursively call opposite function at a lower depth
                    alpha = max(alpha, self.min_value(state, depth-1, alpha, beta))
                    if (alpha >= beta):
                        return beta
                return alpha

    def min_value(self, state, depth, alpha, beta):
        if (self.game_value(state) != 0):
            return self.game_value(state)
        elif depth == 0:
            return self.heuristic_game_value(state)
        else:
            pieces = 0
            for row in state:
                pieces += row.count('b') + row.count('r')
            if(pieces >= 8):
                #move phase
                succs = self.move_phase_succ(state, self.opp)
                for succ in succs:
                    temp_state = copy.deepcopy(state)
                    temp_state[succ[0][0]][succ[0][1]] = self.opp
                    temp_state[succ[1][0]][succ[1][1]] = ' '
                    #recursively call opposite function at a lower depth
                    beta = min(beta, self.max_value(state, depth-1, alpha, beta))
                    if (alpha >= beta):
                        return alpha
                return beta
            else:
                #drop phase#
                succs = self.drop_phase_succ(state)
                for succ in succs:
                    temp_state = copy.deepcopy(state)
                    temp_state[succ[0]][succ[1]] = self.my_piece
                    #recursively call opposite function at a lower depth
                    beta = min(beta, self.max_value(temp_state, depth-1, alpha, beta))
                    if (alpha >= beta):
                        return alpha
                return beta


    def opponent_move(self, move):
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def heuristic_game_value(self, state):
        # check for terminal state
        if(self.game_value(state) != 0):
            return self.game_value(state)

        # initilize min and max values to numbers that will be overwritten later
        max_value = float('-inf')
        min_value = float('inf')

        # horizontal- count the number of pieces by the player and the opponent in any given row of 4
        for row in state:
            for col in range(2):
                horizontal_check = []
                for i in range(4):
                    horizontal_check.append(row[col+i])

                # multiply by .25 since we are checking 4 pieces at a time, and don't want to have a heuristic above or below 1/-1
                max_horizontal = horizontal_check.count(self.my_piece)*.25
                min_horizontal = horizontal_check.count(self.opp)*.25

                if (max_horizontal > max_value):
                    max_value = max_horizontal
                if (min_horizontal < min_value):
                    min_value = min_horizontal

        #vertical- count the number of pieces by the player and the opponent in any given column of 4
        for col in range(5):
            for row in range(2):
                vertical_check = []
                for i in range(4):
                    vertical_check.append(state[row+i][col])
                max_vertical = vertical_check.count(self.my_piece)*.25
                min_vertical = vertical_check.count(self.opp)*.25
                if (max_vertical > max_value):
                    max_value = max_vertical
                if (min_vertical < min_value):
                    min_value = min_vertical

        #/ diagonal- count the number of pieces by the player and the opponent in any given north-eastern diagonal of 4, if it doesn't go out of bounds
        for row in range(2):
            for col in range(2):
                ne_diagonal_check = []
                for i in range(4):
                    """check for out of bounds"""
                    if row+i < 5 and col+i < 5:
                        ne_diagonal_check.append(state[row+i][col+i])
                max_ne_diagonal = ne_diagonal_check.count(self.my_piece)*.25
                min_ne_diagonal = ne_diagonal_check.count(self.opp)*.25
                if (max_ne_diagonal > max_value):
                    max_value = max_ne_diagonal
                if (min_ne_diagonal < min_value):
                    min_value = min_ne_diagonal

        #\ diagonal- count the number of pieces by the player and the opponent in any given south-eastern diagonal of 4, if it doesn't go out of bounds
        for row in range(2):
            for col in range(2):
                se_diagonal_check = []
                for i in range(4):
                    """check for out of bounds"""
                    if row+i < 5 and col-i >= 0:
                        se_diagonal_check.append(state[row+i][col-i])
                max_se_diagonal = se_diagonal_check.count(self.my_piece)*.25
                min_se_diagonal = se_diagonal_check.count(self.opp)*.25
                if (max_se_diagonal > max_value):
                    max_value = max_se_diagonal
                if (min_se_diagonal < min_value):
                    min_value = min_se_diagonal
                    
        #square- count the number of pieces by the player and the opponent in any given 2x2 square
        for row in range(4):
            for col in range(4):
                square_check = []
                for i in range(2):
                    for j in range(2):
                        square_check.append(state[row+i][col+j])
                max_square = square_check.count(self.my_piece)*.25
                min_square = square_check.count(self.opp)*.25
                if (max_square > max_value):
                    max_value = max_square
                if (min_square < min_value):
                    min_value = min_square
        
        return max_value + min_value

    # This function checks for terminal states within the game.
    def game_value(self, state):
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col + 3] != ' ' and state[row][col + 3] == state[row + 1][col + 2] == state[row + 2][col + 1] == state[row + 3][col]:
                    return 1 if state[row][col + 3] == self.my_piece else -1

        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col + 1] == state[row + 1][col] == state[row + 1][col + 1]:
                    return 1 if state[row][col] == self.my_piece else -1
        return 0  # no winner yet
