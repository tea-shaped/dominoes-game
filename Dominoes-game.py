
def create_dominoes_game(rows, cols):
    board = []
    for y in range(rows):
        temp = []
        for x in range(cols):
            temp.append(False)
        board.append(temp)
    return DominoesGame(board)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c] = False

    def is_legal_move(self, row, col, vertical):
        result = False
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if not vertical:
                if col + 1 < self.cols and not self.board[row][col] and not \
                        self.board[row][col + 1]:
                    result = True
            if vertical:
                if row + 1 < self.rows and not self.board[row][col] and not \
                        self.board[row + 1][col]:
                    result = True

        return result

    def legal_moves(self, vertical):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.is_legal_move(r, c, vertical):
                    yield r, c

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if not vertical:
                self.board[row][col + 1] = True
                self.board[row][col] = True
            if vertical:
                self.board[row + 1][col] = True
                self.board[row][col] = True

    def game_over(self, vertical):
        if not list(self.legal_moves(vertical)):
            return True
        return False

    def copy(self):
        board = []
        for r in self.board:
            board.append(r[:])
        copy = DominoesGame(board)
        return copy

    def successors(self, vertical):
        for m in self.legal_moves(vertical):
            x, y = m
            game = self.copy()
            game.perform_move(x, y, vertical)
            yield (x, y), game

    def get_random_move(self, vertical):
        pass

    # Required
    def get_best_move(self, vertical, limit):
        is_max = True
        return self.alpha_beta(is_max, None, vertical, limit, -float('inf'),
                               float('inf'))

    def alpha_beta(self, is_max, m, vertical, limit, alpha, beta):
        i = 0
        move = m
        if is_max:
            val = float('-inf')
            if self.game_over(vertical) or limit == 0:
                temp = len(list(self.successors(vertical))) - len(
                    list(self.successors(not vertical)))
                return move, temp, 1

            for x, y in list(self.successors(vertical)):
                _, temp, cnt = y.alpha_beta(not is_max, x, not vertical,
                                            limit - 1, alpha, beta)
                i = i + cnt
                if temp > val:
                    val = temp
                    move = x
                if val >= beta:
                    return move, val, i
                if val > alpha:
                    alpha = val

        if not is_max:
            val = float('inf')
            if self.game_over(vertical) or limit == 0:
                temp = len(list(self.successors(not vertical))) - len(
                    list(self.successors(vertical)))
                return move, temp, 1

            for x, y in list(self.successors(vertical)):
                _, temp, cnt = y.alpha_beta(not is_max, x, not vertical,
                                            limit - 1, alpha, beta)
                i = i + cnt
                if temp < val:
                    val = temp
                    move = x
                if val <= alpha:
                    return move, val, i
                if val < beta:
                    beta = val

        return move, val, i

