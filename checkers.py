import copy
import math
import time
import json
import os


class BoardEnv:
    JUMP = "JUMP"
    SIMPLE = "SIMPLE"
    WHITE = "WHITE"
    BLACK = "BLACK"

    def __init__(self, board=None, color=None):
        if board is None:
            self.board = []
        else:
            self.board = board
        if color == self.WHITE:
            self.is_white = True
        else:
            self.is_white = False
        self.set_piece_pos()

    def set_piece_pos(self):
        self.pos_W = []
        self.pos_w = []
        self.pos_B = []
        self.pos_b = []
        for i in range(0, 8):
            for j in range(0, 8):
                # if (i + j) % 2 == 1:
                if self.board[i][j] == 'W':
                    self.pos_W.append((i, j))
                elif self.board[i][j] == 'w':
                    self.pos_w.append((i, j))
                elif self.board[i][j] == 'B':
                    self.pos_B.append((i, j))
                elif self.board[i][j] == 'b':
                    self.pos_b.append((i, j))

    def move(self, from_pos, to_pos, move_type):
        new_board = copy.deepcopy(self.board)
        new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
        if self.is_white:
            if to_pos[0] == 0:
                new_board[to_pos[0]][to_pos[1]] = new_board[to_pos[0]][to_pos[1]].upper()
            color = self.WHITE
        else:
            if to_pos[0] == 7:
                new_board[to_pos[0]][to_pos[1]] = new_board[to_pos[0]][to_pos[1]].upper()
            color = self.BLACK

        new_board[from_pos[0]][from_pos[1]] = '.'

        if move_type == self.JUMP:
            if to_pos[0] > from_pos[0]:
                d_row = from_pos[0] + 1
            else:
                d_row = from_pos[0] - 1
            if to_pos[1] > from_pos[1]:
                d_col = from_pos[1] + 1
            else:
                d_col = from_pos[1] - 1
            new_board[d_row][d_col] = '.'

        return BoardEnv(new_board, color)

    def get_potential_moves(self, pos, move_type):

        if self.is_white:
            opp_c = 'b'
        else:
            opp_c = 'w'
        potential_moves = []

        if self.is_white or (not self.is_white and self.board[pos[0]][pos[1]] == 'B'):  # pawn movement bottom to up

            if move_type == self.JUMP:
                if pos[0] - 2 >= 0:
                    if pos[1] + 2 < 8 and (
                            self.board[pos[0] - 1][pos[1] + 1] == opp_c or self.board[pos[0] - 1][
                        pos[1] + 1] == opp_c.upper()) and \
                            self.board[pos[0] - 2][pos[1] + 2] == '.':
                        potential_moves.append((pos[0] - 2, pos[1] + 2))
                    if pos[1] - 2 >= 0 and (
                            self.board[pos[0] - 1][pos[1] - 1] == opp_c or self.board[pos[0] - 1][
                        pos[1] - 1] == opp_c.upper()) and \
                            self.board[pos[0] - 2][pos[1] - 2] == '.':
                        potential_moves.append((pos[0] - 2, pos[1] - 2))

            elif move_type == self.SIMPLE:
                if pos[0] - 1 >= 0:
                    if pos[1] + 1 < 8 and self.board[pos[0] - 1][pos[1] + 1] == '.':
                        potential_moves.append((pos[0] - 1, pos[1] + 1))
                    if pos[1] - 1 >= 0 and self.board[pos[0] - 1][pos[1] - 1] == '.':
                        potential_moves.append((pos[0] - 1, pos[1] - 1))

        if (self.is_white and self.board[pos[0]][pos[1]] == 'W') or (not self.is_white):  # pawn movement top to down

            if move_type == self.JUMP:
                if pos[0] + 2 < 8:
                    if pos[1] + 2 < 8 and (
                            self.board[pos[0] + 1][pos[1] + 1] == opp_c or self.board[pos[0] + 1][
                        pos[1] + 1] == opp_c.upper()) and \
                            self.board[pos[0] + 2][pos[1] + 2] == '.':
                        potential_moves.append((pos[0] + 2, pos[1] + 2))
                    if pos[1] - 2 >= 0 and (
                            self.board[pos[0] + 1][pos[1] - 1] == opp_c or self.board[pos[0] + 1][
                        pos[1] - 1] == opp_c.upper()) and \
                            self.board[pos[0] + 2][pos[1] - 2] == '.':
                        potential_moves.append((pos[0] + 2, pos[1] - 2))

            elif move_type == self.SIMPLE:
                if pos[0] + 1 < 8:
                    if pos[1] + 1 < 8 and self.board[pos[0] + 1][pos[1] + 1] == '.':
                        potential_moves.append((pos[0] + 1, pos[1] + 1))
                    if pos[1] - 1 >= 0 and self.board[pos[0] + 1][pos[1] - 1] == '.':
                        potential_moves.append((pos[0] + 1, pos[1] - 1))

        return potential_moves

    def get_jump_sequence(self, from_pos, to_pos, moves):
        new_board_env = self.move(from_pos, to_pos, self.JUMP)
        moves.append(("J", from_pos, to_pos))
        results = []

        # if pawn reaches end of board on opponent's side, and if it's crowned King, then turn ends. Stop jumps.
        if self.board[from_pos[0]][from_pos[1]].islower() and new_board_env.board[to_pos[0]][to_pos[1]].isupper():
            if (self.is_white and to_pos[0] == 0) or (not self.is_white and to_pos[0] == 7):
                results.append((new_board_env, moves))
                return results
        # check if you can jump the same pawn again

        potential_moves = new_board_env.get_potential_moves(to_pos, self.JUMP)
        if not potential_moves:
            results.append((new_board_env, moves))
        for to_pos2 in potential_moves:
            results.extend(new_board_env.get_jump_sequence(to_pos, to_pos2, moves[:]))
        return results

    def get_moves(self, move_type):
        if self.is_white:
            pos = self.pos_w + self.pos_W
        else:
            pos = self.pos_b + self.pos_B

        results = []
        for from_pos in pos:  # for each pawn on the board
            for to_pos in self.get_potential_moves(from_pos, move_type):  # get potential jump positions

                if move_type == self.JUMP:
                    for board, moves in self.get_jump_sequence((from_pos[0], from_pos[1]), (to_pos[0], to_pos[1]),
                                                               []):  # for each jump position, get the jump sequence
                        results.append((board, moves))

                elif move_type == self.SIMPLE:
                    board = self.move(from_pos, to_pos, move_type)
                    results.append((board, [("E", from_pos, to_pos)]))

        return results

    def eval_function(self, color):
        eval = len(self.pos_w) + (len(self.pos_W) * 2) - len(self.pos_b) - (len(self.pos_B) * 2)
        if color == self.WHITE:
            return eval
        else:
            return -eval

    def action_space(self):
        results = self.get_moves(self.JUMP)
        if not results:
            results = self.get_moves(self.SIMPLE)
        return results


class CheckerSolver:
    SINGLE = "SINGLE"
    GAME = "GAME"
    NUM_PIECES = 24
    MAX_MOVES = 75

    def get_num_moves_left(self):
        _file_name = "playdata.txt"
        if os.path.exists(_file_name):
            with open(_file_name, "r") as f:
                return int(f.read())

        self.set_num_moves_left(self.MAX_MOVES)
        return self.MAX_MOVES

    def set_num_moves_left(self, value):
        _file_name = "playdata.txt"
        with open(_file_name, "w") as f:
            f.write(str(value))

    @classmethod
    def from_file(cls, input_file="input.txt"):
        obj = cls()
        obj.start_time = time.time()
        with open(input_file, "r") as input_f:
            lines = [line.rstrip() for line in input_f.readlines()]
            obj.game_type = lines[0]
            obj.color = lines[1]
            obj.time = float(lines[2])
            b = []
            for i in range(3, 11):
                b.append(list(lines[i]))

        obj.boardEnv = BoardEnv(b, obj.color)
        return obj

    @classmethod
    def from_array(cls, board, color):
        obj = cls()
        obj.start_time = time.time()
        obj.game_type = CheckerSolver.GAME
        obj.color = color
        obj.time = math.inf
        obj.boardEnv = BoardEnv(board, color)
        return obj

    @staticmethod
    def write_output(actions, output_file="output.txt"):
        with open(output_file, "w") as output_f:
            result = []
            for action in actions:
                from_r = 8 - action[1][0]
                from_c = chr(ord('a') + action[1][1])
                to_r = 8 - action[2][0]
                to_c = chr(ord('a') + action[2][1])
                result.append(f"{action[0]} {from_c}{from_r} {to_c}{to_r}")
            output_f.write("\n".join(result))

    def alpha_beta(self, depth, is_calibrating=False):
        v, new_b, actions = self.max_value(self.boardEnv, -math.inf, math.inf, depth)
        CheckerSolver.write_output(actions)
        return v, new_b, actions  # actions to next state with value v

    def max_value(self, b: BoardEnv, alpha, beta, depth):
        if depth == 0:
            return b.eval_function(self.color), [], []
        v = -math.inf
        ret_new_b = None
        ret_actions = []
        for new_b, actions in b.action_space():
            assert isinstance(new_b, BoardEnv)
            new_b.is_white = not new_b.is_white
            _v = self.min_value(new_b, alpha, beta, depth - 1)
            if _v > v:
                ret_new_b = new_b
                ret_actions = actions
            v = max(v, _v)
            if v >= beta:
                return v, new_b, actions
            alpha = max(alpha, v)
        return v, ret_new_b, ret_actions

    def min_value(self, b: BoardEnv, alpha, beta, depth):
        if depth == 0:
            return b.eval_function(self.color)
        v = math.inf
        for new_b, actions in b.action_space():
            new_b.is_white = not new_b.is_white
            _v, _, _ = self.max_value(new_b, alpha, beta, depth - 1)
            v = min(v, _v)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    @property
    def game_state(self):
        total_pawns = len(self.boardEnv.pos_b + self.boardEnv.pos_B + self.boardEnv.pos_w + self.boardEnv.pos_W)
        if total_pawns >= self.NUM_PIECES:
            return "initial"
        if 23 >= total_pawns >= 18:  # 18-23 pawns remaining
            return "start"
        elif 17 >= total_pawns >= 10:  # 10-17
            return "mid"
        return "end"

    def play_game(self):
        if self.game_type == CheckerSolver.SINGLE:
            results = self.boardEnv.action_space()
            CheckerSolver.write_output(results[0][1])
        else:
            num_rounds_left = self.get_num_moves_left()
            self.set_num_moves_left(num_rounds_left - 1)
            time_allotted_for_move = self.time / max(30, num_rounds_left)
            self.boardEnv.set_piece_pos()
            # if the board is full, set the depth to 2
            if self.game_state == "initial":
                depth = 3
            else:
                with open("calibration.txt", "r") as f:
                    calibration = json.load(f)[self.game_state]
                    depth = 3
                    for calibration_depth in calibration:
                        if calibration[calibration_depth] < time_allotted_for_move:
                            depth = max(depth, int(calibration_depth))
            depth = 3

            v, new_b, actions = self.alpha_beta(depth)

            if not actions == []:
                CheckerSolver.write_output(actions)
            else:
                # if alpha_beta doesn't return an action (in case losing is inevitable), return random
                results = self.boardEnv.action_space()
                CheckerSolver.write_output(results[0][1])


if __name__ == "__main__":
    start = time.time()
    c = CheckerSolver.from_file()
    c.play_game()



