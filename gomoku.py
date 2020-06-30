import math
import copy
import random
import time

BOARD_SIZE = 19
WHITE = 'O'
BLACK = 'X'
INF = math.inf
DIRECTIONS = [(1, -1), (1, 0), (1, 1), (0, 1)]  # row, col
ACTION_TO_VALUE = {}


def not_player(player):
    if player == WHITE:
        return BLACK
    else:
        return WHITE


def board_place(board, col, row, player):
    if col < 0 or col > BOARD_SIZE - 1 or row < 0 or row > BOARD_SIZE - 1:
        return False
    new_board = copy.deepcopy(board)
    new_board[row][col] = player
    return new_board


def result(state, col, row, player):
    return board_place(state, col, row, player)


def cutoff_test(depth, time_variable):
    start_time, time_limit = time_variable[0], time_variable[1]
    endTime = time.time() - start_time
    if endTime > time_limit:
        return True
    if depth <= 0:
        return True
    else:
        return False


def safe_bound(col: int, row: int) -> bool:
    if col < 0 or col > BOARD_SIZE - 1 or row < 0 or row > BOARD_SIZE - 1:
        return False
    else:
        return True


# XXXXX
def condition_five_in_row(state: object, col: int, row: int, d_col: int, d_row: int, player: str) -> int:
    res = 0
    if (player == state[row][col] == state[row + d_row * 1][col + d_col * 1] == state[row + d_row * 2][
            col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] == state[row + d_row * 4][col + d_col * 4]):
        res += 1
    return res


# _XXXX_
def condition_four_in_row_low(state, col, row, d_col, d_row, player):
    res = 0
    if (state[row][col] == '_' and player == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] ==
            state[row + d_row * 4][col + d_col * 4] and state[row + d_row * 5][col + d_col * 5] == '_'):
        res += 1
    return res


# _XXXXO(_XXXX|) or OXXXX_(|XXXX_)
def condition_four_in_row(state, col, row, d_col, d_row, player):
    res = 0
    if (state[row][col] == '_' and player == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] ==
            state[row + d_row * 4][col + d_col * 4] and
            state[row + d_row * 5][col + d_col * 5] == not_player(player)):
        res += 1
    if (state[row][col] == not_player(player) and player == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] ==
            state[row + d_row * 4][col + d_col * 4] and
            state[row + d_row * 5][col + d_col * 5] == '_'):
        res += 1
    # TODO: scalar별로 categorize
    if (row == 0 and col == 0 and player == state[row][col] == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] and
            state[row + d_row * 4][col + d_col * 4] == '_'):
        res += 1
    if (row == 0 and (d_row, d_col) != (0, 1)
            and player == state[row][col] == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] and
            state[row + d_row * 4][col + d_col * 4] == '_'):
        res += 1
    if (col == 0 and (d_row, d_col) != (-1, 0)
            and player == state[row][col] == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] and
            state[row + d_row * 4][col + d_col * 4] == '_'):
        res += 1
    return res


# _XXX_ 만 counting
def condition_three_in_row(state, col, row, d_col, d_row, player):
    res = 0
    if (state[row][col] == '_' and player == state[row + d_row * 1][col + d_col * 1] == state[row + d_row * 2][
            col + d_col * 2] == state[row + d_row * 3][col + d_col * 3] and state[row + d_row * 4][col + d_col * 4] == '_'):
        res += 1
    return res


# _XXXO(_XXX| or OXXX_ (|XXX_)
def condition_three_in_row_low(state, col, row, d_col, d_row, player):
    res = 0
    if (state[row][col] == not_player(player) and player == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col *
                                   2] == state[row + d_row * 3][col + d_col * 3]
            and state[row + d_row * 4][col + d_col * 4] == '_'):
        res += 1
    if (state[row][col] == '_' and player == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col *
                                   2] == state[row + d_row * 3][col + d_col * 3]
            and state[row + d_row * 4][col + d_col * 4] == not_player(player)):
        res += 1
    if (row == 0 and col == 0
            and player == state[row][col] == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2]
            and state[row + d_row * 3][col + d_col * 3] == '_'):
        res += 1
    if (row == 0 and (d_row, d_col) != (0, 1)
            and player == state[row][col] == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2]
            and state[row + d_row * 3][col + d_col * 3] == '_'):
        res += 1
    if (col == 0 and (d_row, d_col) != (-1, 0)
            and player == state[row][col] == state[row + d_row * 1][col + d_col * 1] ==
            state[row + d_row * 2][col + d_col * 2]
            and state[row + d_row * 3][col + d_col * 3] == '_'):
        res += 1
    return res


# _XX_
def condition_two_in_row(state, col, row, d_col, d_row, player):
    res = 0
    if (state[row][col] == '_' and player == state[row + d_row * 1][col + d_col * 1] == state[row + d_row * 2][
            col + d_col * 2] and state[row + d_row * 3][col + d_col * 3] == '_'):
        res += 1
    return res


# _XXO OXX_
def condition_two_in_row_low(state, col, row, d_col, d_row, player):
    res = 0
    if (state[row][col] == '_'
            and player == state[row + d_row * 1][col + d_col * 1] == state[row + d_row * 2][col + d_col * 2]
            and state[row + d_row * 3][col + d_col * 3] == not_player(player)):
        res += 1
    if (state[row][col] == not_player(player)
            and player == state[row + d_row * 1][col + d_col * 1] == state[row + d_row * 2][col + d_col * 2]
            and state[row + d_row * 3][col + d_col * 3] == '_'):
        res += 1
    return res


# _X_ _XO OX_
def condition_non_threat(state, col, row, d_col, d_row, player):
    res = 0
    if (state[row][col] == '_'
            and player == state[row + d_row * 1][col + d_col * 1]
            and state[row + d_row * 2][col + d_col * 2] == '_'):
        res += 1
    if (state[row][col] == '_'
            and player == state[row + d_row * 1][col + d_col * 1]
            and state[row + d_row * 2][col + d_col * 2] == not_player(player)):
        res += 1
    if (state[row][col] == not_player(player)
            and player == state[row + d_row * 1][col + d_col * 1]
            and state[row + d_row * 2][col + d_col * 2] == '_'):
        res += 1
    return res


def precondition(col, row, d_col, d_row, scalar):
    if safe_bound(col + d_col * scalar, row + d_row * scalar):
        return True
    else:
        return False


def count_current_position(state, col, row, player):
    w1, w2, w3, w4, w5, w6, w7, w8 = 0, 0, 0, 0, 0, 0, 0, 0

    for d_row, d_col in DIRECTIONS:
        if precondition(col, row, d_col, d_row, 4):
            w1 += condition_five_in_row(state, col, row, d_col, d_row, player)
        if precondition(col, row, d_col, d_row, 5):
            w2 += condition_four_in_row_low(state,
                                            col, row, d_col, d_row, player)
        if precondition(col, row, d_col, d_row, 5):
            w3 += condition_four_in_row(state, col, row, d_col, d_row, player)
        if precondition(col, row, d_col, d_row, 4):
            w4 += condition_three_in_row(state, col, row, d_col, d_row, player)
        if precondition(col, row, d_col, d_row, 4):
            w5 += condition_three_in_row_low(state,
                                             col, row, d_col, d_row, player)
        if precondition(col, row, d_col, d_row, 3):
            w6 += condition_two_in_row(state, col, row, d_col, d_row, player)
        if precondition(col, row, d_col, d_row, 3):
            w7 += condition_two_in_row_low(state,
                                           col, row, d_col, d_row, player)
        if precondition(col, row, d_col, d_row, 2):
            w8 += condition_non_threat(state, col, row, d_col, d_row, player)
    return w1, w2, w3, w4, w5, w6, w7, w8


def eval_state(state, player):
    f1, f2, f3, f4, f5, f6, f7, f8 = 0, 0, 0, 0, 0, 0, 0, 0
    for row in range(0, BOARD_SIZE):
        for col in range(0, BOARD_SIZE):
            if not check_neighbor(col, row, state):
                continue
            ww1, ww2, ww3, ww4, ww5, ww6, ww7, ww8 = \
                count_current_position(state, col, row, player)
            f1 += ww1
            f2 += ww2
            f3 += ww3
            f4 += ww4
            f5 += ww5
            f6 += ww6
            f7 += ww7
            f8 += ww8
        pass
    pass

    w1 = 50000000  # 1) XXXXX
    w2 = 5005000  # 2) _XXXX_
    w3 = 500500  # 3) _XXXXO(_XXXX|) or OXXXX_(|XXXX_)
    w4 = 100050  # 4) _XXX_ 만 counting
    w5 = 10000  # 5) _XXXO(_XXX| or OXXX_ (|XXX_)
    w6 = 1000  # 6) _XX_
    w7 = 10  # 7) _XXO OXX_
    w8 = 1  # 8) _X_ _XO OX_

    res = f1 * w1 + f2 * w2 + f3 * w3 + f4 * \
        w4 + f5 * w5 + f6 * w6 + f7 * w7 + f8 * w8
    return res


def make_movable_actions(state, player):
    actions = []
    actions.clear()
    for row in range(0, BOARD_SIZE):
        for col in range(0, BOARD_SIZE):
            if state[row][col] != '_':
                continue
            if not check_neighbor(col, row, state):
                continue
            if gomoku_rule_samsam(state, col, row, player):
                continue
            actions.append((row, col))
        pass
    if len(actions) < 1:  # 군집 구역이 없는 경우 == 첫 수를 두는 경우
        row, col = random.randrange(
            0, BOARD_SIZE), random.randrange(0, BOARD_SIZE)
        actions.append((row, col))
    random.shuffle(actions)
    return actions


def gomoku_rule_samsam(state, col, row, player):
    new_state = board_place(state, col, row, player)
    ds = [(-1, -1), (1, 1),
          (-1, 0), (1, 0),
          (-1, 1), (1, -1),
          (0, -1), (0, 1)]
    cnt = 0
    for d in ds:
        d_r = d[0]
        d_c = d[1]
        if (safe_bound(row - d_r, row + d_c) and safe_bound(row + d_r * 3, col + d_c * 3) and
                new_state[row - d_r][col + d_c] == '_' and new_state[row][col] == new_state[row + d_r][col + d_c] ==
                new_state[row + 2 * d_r][col + 2 * d_c] and new_state[row + 3 * d_r][col + 3 * d_c] == '_'):
            cnt += 1
    return cnt >= 2


def check_neighbor(col, row, state):
    # 좌상 좌 좌하 하 우하 우 우상 상
    ds = [(-1, -1), (1, 1),
          (-1, 0), (1, 0),
          (-1, 1), (1, -1),
          (0, -1), (0, 1)]
    for d in ds:
        r = d[0]
        c = d[1]
        if safe_bound(col + c, row + r):
            if state[row + r][col + c] != '_':
                return True
            else:
                pass
        else:
            pass
    return False


def eval_minimax(state, player):
    myV = eval_state(state, player)
    yourV = eval_state(state, not_player(player))
    return myV - yourV


def alpha_beta_search_IDS(state, player, depth, time_variable):
    start_time, time_limit = time_variable[0], time_variable[1]
    v = -INF
    alpha, beta = -INF, INF
    actions = []
    if len(ACTION_TO_VALUE) == 0:
        actions = make_movable_actions(state, player)
    else:  # 이미 계산했던 것이라면 최대한 VALUE가 높았던 순서대로 탐색 시도.
        actions = list(map(lambda x: x[0], sorted(
            ACTION_TO_VALUE.items(), key=lambda x: x[1], reverse=True)))
    for action in actions:
        endTime = time.time() - start_time
        if endTime > time_limit:
            break
        row = action[0]
        col = action[1]
        vv = min_value_IDS(result(state, col, row, player),
                           alpha, beta, depth - 1, player, time_variable)
        ACTION_TO_VALUE[action] = vv
        v = max(v, vv)
        if v >= beta:  # upper bound
            break
        alpha = max(alpha, v)

    for action, value in ACTION_TO_VALUE.items():
        if value == v:
            return action

    random_move = random.choices(actions)  # 최적해가 존재하지 않는 경우. (발생 X)
    return random_move  # the action in ACTIONS(state) with value v


def min_value_IDS(state, alpha, beta, depth, player, time_variable):
    if cutoff_test(depth, time_variable):
        return eval_minimax(state, player)
    else:
        v = INF
        actions = make_movable_actions(state, player)
        for action in actions:
            row = action[0]
            col = action[1]
            v = min(v, max_value_IDS(result(state, col, row, not_player(player)), alpha, beta, depth - 1, player,
                                     time_variable))
            if v <= alpha:  # lower bound
                return v
            beta = min(beta, v)
        return v


def max_value_IDS(state, alpha, beta, depth, player, time_variable):
    if cutoff_test(depth, time_variable):
        return eval_minimax(state, player)
    else:
        v = -INF
        actions = make_movable_actions(state, player)
        for action in actions:
            row = action[0]
            col = action[1]
            v = max(v, min_value_IDS(result(state, col, row, player),
                                     alpha, beta, depth, player, time_variable))
            if v >= beta:  # upper bound
                return v
            alpha = max(alpha, v)
        return v  # utility value


def depth_limit_search(problem_state, player, depth, time_limit):
    start_time = time.time()
    return alpha_beta_search_IDS(problem_state, player, depth, (start_time, time_limit))


def iterative_deepening_search(state, player, selected_limit, time_limit):
    ACTION_TO_VALUE.clear()  # action_to_values 값을 초기화
    depth_limit = selected_limit + 1  # IDS의 depth_limit. difficulty와 관련있는 변수.
    search_result = []
    for depth in range(1, depth_limit):
        search_result = depth_limit_search(state, player, depth, time_limit)
    return search_result


class Problem:
    def __init__(self, initial_state=None):
        if initial_state is None:
            initial_state = [["_" for i in range(19)] for j in range(19)]
        self.state = initial_state
        self.my_colour = BLACK
        self.ai_colour = WHITE
        self.depth_limit = 2
        self.time_limit = 10

    def put_stone(self, row, col, player):
        new_state = board_place(self.state, col, row, player)
        if new_state:
            self.state = new_state
        else:
            print("ERROR")
            return False

    def display(self):
        print('r,c\t', end='')
        for col in range(BOARD_SIZE):
            print('{:3}'.format(col), end='')
        print()
        for row in range(BOARD_SIZE):
            print('{:2}|\t'.format(row), end='')
            for col in range(BOARD_SIZE):
                print('{:>3}'.format(self.state[row][col]), end='')
            print()

    def put_able(self, row, col, player):
        return safe_bound(row, col) and self.state[row][col] == '_' and not gomoku_rule_samsam(self.state, row, col,
                                                                                               player)

    def start(self):
        # 게임 시작한다고 알려주기.
        # 팀 선택하기
        print('오목 게임을 시작합니다.')
        while True:
            print('1. AI의 search_depth (2 ply 당 1 depth)를 선택하세요')
            print('-- 큰 값일 수록 오래 걸립니다.')
            print('-- 2를 추천합니다. 2는 5초 이내로 탐색을 완료합니다.')
            print('-- 2보다 클 경우 시간제한을 벗어날 수 있습니다.')
            print('-- 1 ~ 5 ')
            print()
            depth_limit: int = int(input('>> '))
            if 1 <= depth_limit <= 5:
                self.depth_limit = depth_limit
                break
            else:
                print('1 ~ 3 사이의 값만 입력해주세요.')
        print()
        while True:
            print('2. AI의 탐색 제한 시간을 설정해주세요.')
            print('-- 5 ~ 120초')
            print('-- e.g. 10 : 10초의 제한시간')
            print()
            time_limit: int = int(input('>> '))
            if 1 <= time_limit <= 120:
                self.time_limit = time_limit
                break
            else:
                print('너무 오래걸리는 제한입니다. 다시 생각해보세요.')
        print('depth_limit:{}, time_limit:{}로 설정되었습니다.'.format(
            depth_limit, time_limit))
        print()

    def choose_team(self):
        while True:
            print('3. 색을 선택하세요.')
            print('-- 1.BLACK')
            print('-- 2.WHITE')
            print()
            colour: int = int(input('>> '))
            if colour == 1 or colour == 2:
                self.my_colour = BLACK if colour == 1 else WHITE
                self.ai_colour = not_player(self.my_colour)
                break
            else:
                print('1 ~ 2 두 값 중 하나만 입력해주세요.')
        print('색상이 {}로 선택됐습니다.'.format(self.my_colour))
        print('자동으로 AI는 {}으로 설정됩니다.'.format(self.ai_colour))

    def one_turn(self, current_player):
        # 선택된 current_player에 따라서 player_turn 혹은 ai_turn 실행
        if current_player == self.my_colour:
            self.player_turn()
        else:
            self.ai_turn()
        pass

    def player_turn(self):
        while True:
            print('[USER] 어디에 두실건가요?')
            row, col = map(int, input('>> ').split())
            if self.put_able(row, col, self.my_colour):
                self.put_stone(row, col, self.my_colour)
                break
            else:
                print('둘 수 없는 곳입니다.')
        print('[USER] ({}, {})에 두었습니다.'.format(row, col))

    def ai_turn(self):
        next_move = iterative_deepening_search(
            self.state, self.ai_colour, self.depth_limit, self.time_limit)
        print('[AI]삐빅...삐빅..AI는 (', next_move, ')로 움직이기를 원함.')
        self.put_stone(next_move[0], next_move[1], self.ai_colour)
        print('[AI] ({}, {})에 두었습니다.'.format(next_move[0], next_move[1]))

    def is_over(self, player):
        winning_row = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                for d_row, d_col in DIRECTIONS:
                    if precondition(c, r, d_col, d_row, 4):
                        winning_row += condition_five_in_row(
                            self.state, c, r, d_col, d_row, player)
        if winning_row != 0:
            return True
        else:
            return False


init_state = [["_" for i in range(19)] for j in range(19)]

print('python의 특성상 속도가 느립니다. pypy3로 구동한다면 더 빠른 속도를 체감할 수 있습니다.')

game = Problem(init_state)
game.start()  # 게임 시작. search_depth와 time_limit 설정
game.choose_team()  # 팀 설정.
current_player = BLACK
while True:
    game.display()
    game.one_turn(current_player)  # 놓을 곳 선택하기.
    if game.is_over(current_player):
        print('[SYS] 게임이 끝났어요!')
        print('[SYS] 승자는 바로 {}입니다.'.format(current_player))
        break
    current_player = not_player(current_player)

game.display()
print('[SYS] 종료되었습니다~')
