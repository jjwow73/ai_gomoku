# Minimax를 이용해 오목 구현

##### Table of Contents

[초록](##초록)  
[알고리즘](##알고리즘)  
[알고리즘 구현](##알고리즘-구현)  
[후기](##후기)

## 초록

오목은 2명의 사용자가 서로 적대적인 관계를 갖고 경쟁하는 게임으로, 연속적인 5개의 돌을 놓으면 이기는 규칙을 갖고 있다. 이런 형태의 게임을 Adversial Strategy Game이라 한다. 룰에 따라서 종류가 나뉘는데 고모쿠룰, 오목룰, 렌주룰 등이 있다. 일반적인 오목은 19\*19의 크기에서 진행되며 33은 허용하지 않는 규칙을 갖고 있다.

오목은 적대적인 탐색을 활용한 AI를 도입할 수 있는 Game 중 하나로, 사람도 몇 수 앞을 더 내다볼 수 있는 사람이 이길 확률이 높듯이 AI 또한 몇 수 앞까지 내다보느냐에 따라서 난이도가 달라진다. 이 프로젝트는 **COSE361**에서 배웠던 강의 내용과 **Artificial Intelligence: A Modern Approach**를 참고하여 `minimax`, `alpha-beta pruning`, `Evaluation function`, `iterative deepening serach` 등을 활용한 오목 AI이다.

## 알고리즘

### Minimax

게임을 할 때, 나는 나에게 최적의 수를, 상대는 상대에게 최적의 수를 선택한다는 가정을 한 탐색이다. 나에게 최적의 수는 _나의 Max_ 값, 상대에게 최적의 수는 *나의 Min*값이라 한다. 번갈아가며 턴이 돌아간다고 생각한다면 Max(나) -> Min(상대) -> Max(나) -> Min(상대) ... 이렇게 반복되는 것이다.

### Alpha-beta pruning

Minimax 알고리즘이 너무 많은 경우의 수를 계산하는 것을 줄이기 위해 alpha-beta 개념을 적용해야한다. alpha-beta pruning은 가지치기처럼 불필요한 연산을 줄여준다. alpha는 MAX 노드에서 lower bound의 값을 갖고 있고, beta는 MIN 노드에서 upper bound의 값을 갖고 있다. 이 두 수를 이용해 탐색하지 않아도 되는 가지를 제거한다.

아래는 위 두개의 개념을 적용한 **Minimax algorithm with alpha-beta pruning**의 수도코드이다.

<img src=".\img\image-20200630224340618.png" alt="image-20200630224340618" style="zoom:67%;" />

> 출처: Artificial Intelligence: A Modern Approach

### Iterative Deepening Search

IDS(Iterative Deepening Search)는 depth first search의 개념을 확장시킨 탐색으로 depth first search처럼 memory complexity는 $O(b^d)$를 갖고 breadth first search처럼 (braching factor가 유한한 경우) Complete한 탐색을 한다는 장점을 갖고 있다. 이 개념을 이용해 Cutoff나 난이도를 조절할 수 있다.

<img src=".\img\image-20200630224738958.png" alt="image-20200630224738958" style="zoom:67%;" />

### Evaluation Function

오목은 경우의 수가 너무 많기 때문에 완벽한 탐색을 수행할 수 없다. 그렇기 때문에 정해진 조건, 시간이나 탐색 깊이(depth),을 만족하면 종료해야한다. 이때 cutoff가 수행되는데 그때의 state의 utility 값이 해당 state의 cost가 된다. 이 때 state의 utility 값을 반환하는 Evalution Function의 조건은 후술했다.(단순하지만 길다.)

<img src=".\img\image-20200630225559367.png" alt="image-20200630225559367" style="zoom: 67%;" />

## 알고리즘 구현

### minimax with alpha-beta

```python
def min_value_IDS(state, alpha, beta, depth, player, time_variable):
    if cutoff_test(depth, time_variable):
        return eval_minimax(state, player)
    else:
        v = INF
        actions = make_movable_actions(state, player)
        for action in actions:
            row = action[0]
            col = action[1]
            v = min(v, max_value_IDS(result(state, col, row, not_player(player)), alpha, beta, depth - 1, player, time_variable))
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
            v = max(v, min_value_IDS(result(state, col, row, player), alpha, beta, depth, player, time_variable))
            if v >= beta:  # upper bound
                return v
            alpha = max(alpha, v)
        return v  # utility value

```

수도코드와 다른 점은 time_variable이 추가된 점이다. 이 변수는 시간 제한을 주기 위해 전달하는 start_time과 limit_time이다.

처음 실행되는 ALPHA-BETA-SEARCH는 수도코드를 python 코드로 옮기는 데에 어려움이 있어서 조금 다른 접근 방식을 선택했다. 수도코드에서는 MAX_VALUE를 호출하지만 구현물에서는 MAX_VALUE의 함수 동작 자체를 그대로 붙여넣어 동작하도록 했다. 첫 호출의 예외 적용의 이유는 나중에 최종 v값에 해당하는 action을 반환할 수 있게끔 반환된 V 값 마다 대응하는 actions을 저장하는 변수를 만들기 위해서이다. 그런 동작을 하는 변수는 ACTION_TO_VALUE 이다. 이 변수는 전역변수로 선언해서 추후 IDS에서의 시간제한이나 CUTOFF에서 성능향상을 도울 수 있다. 이에 대한 자세한 내용은 후술할 예정이다. 추가적으로 다른 내용은 시간 제한을 위한 start_time 선언 및 초기화를 했고 혹시 모를 최적해 없음 사태를 대비해 random하게 actions중 하나를 선택하게 했지만 make_movable_action에서 이미 예외처리를 했기 때문에 unreachable code이다.

### 기타 함수

그 외 state에 대한 평가값을 반환하는 Evaluation(state)함수, state에 대해 행동가능한 actions를 반환하는 Actions(state), 입력받은 action에 대해 다음 state를 반환하는 Result(state)를 구현했다.

#### Evaluation(state)

RealTime Decision을 지향했기 때문에 Cutoff가 발생했을 경우 Terminal State가 아님에도 utility value를 반환해야 한다. 이를 계산하기 위해 eval_mini(state,player), eval_state(state,player)함수와 추가적으로 조건을 확인하는 함수를 만들었다. eval_mini 함수는 현재 state에서 player의 “expected value”와 enemy의 “expected value”의 차를 반환한다. 그것이 player에게 더 좋은 이익이 되는 값이라 판단했다. expected value를 게산하기 위해 chess의 evaluation과 비슷한, 오목의 features에 따른 가중치를 부여한 weighted linear function을 활용했다.

```python
    w1 = 50000000  # 1) XXXXX
    w2 = 5005000  # 2) _XXXX_
    w3 = 500500  # 3) _XXXXO(_XXXX|) or OXXXX_(|XXXX_)
    w4 = 100050  # 4) _XXX_ 만 counting
    w5 = 10000  # 5) _XXXO(_XXX| or OXXX_ (|XXX_)
    w6 = 1000  # 6) _XX_
    w7 = 10  # 7) _XXO OXX_
    w8 = 1  # 8) _X_ _XO OX_

    res = f1 * w1 + f2 * w2 + f3 * w3 + f4 * w4 + f5 * w5 + f6 * w6 + f7 * w7 + f8 * w8
    return res
```

![image-20200630230644216](.\img\image-20200630230644216.png)

*five_in_row*는 게임의 승리 조건인 5개가 연속으로 있는 경우로, 가중치가 매우 높게 부여됐고 _four_in_row_ 또한 승리와 매우 가깝기 때문에 큰 값에 대응된다. 점점 feature의 중요도가 낮아질수록 가중치 또한 비례해 낮아진다. 이를 위해 사용한 함수는 아래와 같다.

- **count_current_position(state, row, col):** 현재 위치에서 condition\_이름을 모두 확인해 f1 ~ f8를 반환하는 함수

- **condition\_이름(state, row, col)**: (row,col)위치에서feature의 조건을 만족하는지 판단하는 함수

- **eval_state(state, player):** state의 모든 row, col위치에서 player에 대한 count_current_position을 수행한 뒤 weighted linear function을 이용해 expected value를 반환하는 함수.
- **eval_mini(state, player):** 현재 state에 대해 player와 enemy(not player)의 expected value차를 반환하는 함수. 수도코드의 eval(state)함수이다.

#### Actions(state)

- **make_movable_actions(state)**: 현재 state에 대해 수행할 수 있는 actions 을 반환한다. 현재 수행할 수 있는 actions은 state에서 놓을 수 있는 position 이다. 이때 검색되는 노드 수를 줄이기 위해서 일종의 편법을 사용했다. 점수를 얻기 위해선 대부분 군집된 구역, 즉 이웃된 위치에 이미 놓여진 돌이 있는 곳에 놓기 때문에 돌이 모인 부분에서 떨어진 부분은 제외했고. 바둑의 rule를 어기는 곳도 제외했다.(33방지) 추가로 군집된 구역이 없는 경우, 첫수를 두는 경우엔 random하게 선택해서 두도록 했다.
- **result**: transition_model을 반환하는 함수이다. 즉, 현재 state에서 action을 수행했을 때의 결과로 나올 state를 반환해준다. 이 함수는 min_value와 max_value에서 깊이가 깊어질 때 사용된다.

#### 추가적인 구현

- **첫 alpha-beta 에서의 예외**:상기 설명 중 ALPHA-BETA-SEARCH에서 첫번째 호출했을 때는 수도코드와 다르게 작성한 부분이 있다. 이는 반환된 v에 해당하는 action을 저장하기 위해서 ACTION_TO_VALUE를 사용하는 것이다. 이때 depth = 1부터 depth = limit 까지 점점 커지면서 탐색하는 Iterative Deepening Search의 특성상 depth가 깊어질 경우 depth=1에서 계산했던 action을 활용할 수 경우를 나눴다. ACTION_TO_VALUE가 이미 존재, 즉 탐색했었던 경우에는 이미 action이 만들어져있고 그 action에 해당하는 각각의 v가 존재한다. v를 기준으로 내림차순 정렬을 하여 v가 큰 action부터 탐색한다. 이럴 경우 시간제한 등으로 수행중이던 탐색이 중단되어도 그나마 가능성이 높은 action부터 검색했기 때문에 더 효율적인 결과를 반환한다.

- **삼삼 방지**: 얍삽이는 쓰면 안된다. :) 삼삼은 놓을 수 없기 때문에 따로 함수를 만들어 조건을 확인했다. 한 곳에 두었을 경우 그 자리로부터 \_XXX\_가 두 개 동시에 존재하는 경우로서 8방위에 대해 \_XXX\_ 가 존재하는지 확인한다.
- **시간초과와 Cutoff**: 시간 초과를 검증하기 위해 몇몇 함수에서 time_variable이란 변수를 인자로 넘기며 start_time과 time_limit을 넘겨준다. 또한 depth도 인자로 넘겨주며 깊어질수록 depth의 값이 줄어든다. 최종적으론 cutoff 함수에 의해 조건을 검사하게 된다.

## 후기

### 시행착오

실제 핵심 개념을 파이썬 코드로 옮기는 과정은 어렵지 않았다. 하지만 원하는 함수를 구현하거나 변수를 저장하고 갱신하는 과정에서 뜻하는 대로 동작하지 않는 경우가 많았다. 파이썬의 경우 call by assignment의 형식을 따라가기 때문에 result함수에서 새로운 state를 생성할 때 copy라이브러리를 활용한 new_state = copy.deepcopy(state) 를 반환해야한다.

가장 어려웠던 부분은 eval함수에서 state의 expected value을 반환하기 위해 조건을 확인하고 가중치를 각각 다르게 주는 것이었다. 조건을 확인하기 위해서 많은 if문을 썼고 가중치를 계산하기 위해 여러 번 코드를 돌려보는 과정이 길었다. 또한 상대방Ply일때와 내Ply일 때 state의 expected value값이 확실하게 달라지게 하는 것을 구현해낼 수 없어서 동일한 expected value를 주고 depth 를 2ply마다 1씩 작아지도록 했다. 이렇게 함으로써 내가 두는 수 뿐만 아니라 상대방이 둘 수까지 계산해내어 최적의 수를 두는 방법을 확실하게 했다.

처음 구현했을 때는 시간이 너무 오래 걸렸었다. depth=2만 되어도 엄청난 시간이 걸렸고 이 시간을 줄이기 위해서 ACTION_TO_VALUE를 도입하고 make_movable_action 함수에서 가능성이 없는 action을 제외시키는 것을 고안했다. 큰 depth에선 시간이 오래걸리는 것은 마찬가지이지만 몇배나 빨라질 수 있었다.

### 결론과 보완점

Minimax 알고리즘을 python코드로 포팅했고 alpha beta pruning과 시간과 깊이를 고려한 cutoff test, 삼삼 방지, 흑/백 선택을 해내는 기능을 구현했다. 또한 depth_limit, time_limit, color 선택은 게임을 시작할 때 선택할 수 있도록 설계했다. 만들어진 성과물로 depth=1, 2, 3씩 늘려가며 플레이를 해봤고 거의 내가 이겼지만 가끔 잘 못 보고 질 때도 있어서 재밌었다.

아쉬운 점은 속도와 공간상으로 만족할 만한 성능은 아니라고 판단된다. depth=3 (ply = 6)이 되면 Game이 길어질수록 너무나 오래 걸린다. (pypy3기준 1분 이상) 인터넷에서 검색해본 결과 Transition Table을 이용한 방법으로 성능을 향상시킨다고 한다. 즉 Transition Table을 도입한다면 속도를 개선할 여지가 있다. 또한 Eval(state) 함수에서 조건을 검색하는 부분이 오래 걸리는 것 같아 어떻게 향상시킬 수 있을지 고민해봤다. 지금은 (0,0)부터 (18,18)까지 모든 점에 대해 검사를 하는데 위 상기한 features를 검사하는 길이로 구분해서 category로 나눈 뒤 검사가 필요한 구역에서만 category(길이)별로 검사를 한다면 그나마 더 깔끔하고 빠른 검사가 가능할 것으로 생각된다.
