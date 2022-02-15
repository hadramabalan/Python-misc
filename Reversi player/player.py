import copy
class MyPlayer:
    """plays based on position and number of frontier discs made"""
    def __init__(self, my_color, opponent_color):
        self.name = 'rondomar'
        self.my_color = my_color  # either or zero, determines the color of our player
        self.opponent_color = opponent_color  # determines the color of the opponent
        self.directions = self.init_directions()  # vectors for which we will check valid moves

    def is_empty(self, board, r, c):  # check if position is empty
        return board[r][c] == -1

    def is_mine(self, board, r, c):   # check if position has our stone on it
        return board[r][c] == self.my_color

    def is_opponents(self, board, r, c):  # check if position has opponents stone on it
        return board[r][c] == self.opponent_color

    def is_inside(self, board, r, c):  # check if position is on the board
        return 0 <= r and r < len(board) and 0 <= c and c < len(board[0])


# Types of squares
#          0 1 2 3 4 5 6 7
#        0 E C B A A B C E
#        1 C X - - - - X C
#        2 B - S S S S - B
#        3 A - S S S S - A
#        4 A - S S S S - A
#        5 B - S S S S - B
#        6 C X - - - - X C
#        7 E C B A A B C E

    # check what type a square is
    def is_e_square(self, move):
        return(move[0] == 0 or move[0] == 7) and (move[1] == 0 or move[1] == 7)

    def is_c_square(self, move):
        return((move[0] == 0 or move[0] == 7) and (move[1] == 1 or move[1] == 6)) or \
            ((move[0] == 1 or move[0] == 6) and (move[1] == 0 or move[1] == 7))

    def is_b_square(self, move):
        return((move[0] == 2 or move[0] == 5) and (move[1] == 0 or move[1] == 7))or \
              ((move[0] == 0 or move[0] == 7) and (move[1] == 2) or move[1] == 5)

    def is_a_square(self, move):
        return((move[0] == 3 or move[0] == 4) and (move[1] == 0 or move[1] == 7)) or \
              ((move[0] == 0 or move[0] == 7) and (move[1] == 3 or move[1] == 4))

    def is_x_square(self, move):
        return(move[0] == 1 or move[0] == 6) and (move[1] == 1 or move[1] == 6)

    def is_s_square(self, move):
        return(move[0] > 1 and move[0] < 6) and (move[1] > 1 and move[1] < 6)

    def position_value(self, move):
        if self.is_e_square(move):
            return 99
        elif self.is_c_square(move):
            return -8
        elif self.is_b_square(move):
            return 8
        elif self.is_a_square(move):
            return 6
        elif self.is_x_square(move):
            return -24
        elif self.is_s_square(move):
            return 4
        else:
            return -4

    #  check if a disc is adjacent to an empty square
    def is_frontier(self, board, move):
        frontier = False
        for dir in self.directions:
            temp_row = move[0] + dir[0]
            temp_col = move[1] + dir[1]
            if self.is_inside(board, temp_row, temp_col):
                if self.is_empty(board, move[0], move[1]):
                    frontier = True
        return frontier

    def count_frontiers(self, board):
        total = 0
        for row in range(len(board)):
            for col in range(row):
                move = [row, col]
                if self.is_frontier(board, move):
                    total += 1
        return total

    def squares_flipped(self, board, move):
        total_squares_flipped = 0
        for dir in self.directions:
            squares_flipped = 0
            temp_row = move[0] + dir[0]
            temp_col = move[1] + dir[1]
            # check if resulting point is on the board
            if self.is_inside(board, temp_row, temp_col):
                while self.is_opponents(board, temp_row, temp_col):
                    # If the position is opponent's, keep checking
                    temp_row += dir[0]
                    temp_col += dir[1]
                    squares_flipped += 1
                    if self.is_inside(board, temp_row, temp_col):
                        # If there's our stone, flip the opponent's pieces
                        if self.is_mine(board, temp_row, temp_col):
                            for i in range(squares_flipped):
                                temp_row -= 1
                                temp_col -= 1
                                board[temp_row][temp_col] = self.my_color
                    else:
                        break
            total_squares_flipped += squares_flipped
        return total_squares_flipped

    def flip_squares(self, board, move):
        total_squares_flipped = 0
        for dir in self.directions:
            squares_flipped = 0
            temp_row = move[0] + dir[0]
            temp_col = move[1] + dir[1]
            # check if resulting point is on the board
            if self.is_inside(board, temp_row, temp_col):
                while self.is_opponents(board, temp_row, temp_col):
                    # If the position is opponent's, keep checking
                    temp_row += dir[0]
                    temp_col += dir[1]
                    squares_flipped += 1
                    if self.is_inside(board, temp_row, temp_col):
                        # If there's our stone, flip the opponent's pieces
                        if self.is_mine(board, temp_row, temp_col):
                            for i in range(squares_flipped):
                                temp_row -= 1
                                temp_col -= 1
                                board[temp_row][temp_col] = self.my_color
                    else:
                        break
            total_squares_flipped += squares_flipped
        return board


    @staticmethod
    def init_directions():
        dirs = []
        for dir in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            dirs.append(dir)
        return dirs

    def valid_moves(self, board):
        moves_list = []  # We will append valid moves to the list in the form of two element tuples with coordinates
        for row in range(len(board)):           # for every row
            for col in range(len(board[row])):  # for every column
                if self.is_mine(board, row, col):
                    for dir in self.directions:     # for every direction
                        # add the direction vector to coordinates
                        temp_row = row + dir[0]
                        temp_col = col + dir[1]
                        # check if resulting point is on the board
                        if self.is_inside(board, temp_row, temp_col):
                            while self.is_opponents(board, temp_row, temp_col):
                                # if the position is opponents, keep checking until we get a free space or our stone
                                temp_row += dir[0]
                                temp_col += dir[1]
                                if self.is_inside(board, temp_row, temp_col):
                                    # if there's our stone, there's no valid move, so just break
                                    if self.is_mine(board, temp_row, temp_col):
                                        break
                                    # if the position is free, it is a valid move position
                                    if self.is_empty(board, temp_row, temp_col):
                                        moves_list.append((temp_row, temp_col))
                                else:
                                    break
        return moves_list

    def move(self, board):
        valid_moves = self.valid_moves(board)  # find valid moves

        if not valid_moves:  # if there's no valid move, return None
            return None
        else:
            max_value = -1000
            best_move = None

            for move in valid_moves:
                frontier_total = self.count_frontiers(board)
                new_board = copy.deepcopy(board)
                new_board = self.flip_squares(new_board, move)
                new_frontier_total = self.count_frontiers(new_board)
                value = self.position_value(move) + 4 * (frontier_total - new_frontier_total)
                if value > max_value:
                    max_value = value
                    best_move = move

            return best_move



