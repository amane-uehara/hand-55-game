MAX_FINGER_NUM = 3

def get_next_state_list(state):
  curt_turn  = state[0]
  my_bunretu = state[1+curt_turn][0]
  my_hand    = state[1+curt_turn][1]

  next_turn  = 1 - state[0]
  op_bunretu = state[1+next_turn][0]
  op_hand    = state[1+next_turn][1]

  ret = []
  if ((my_hand == (0,0)) or (op_hand == (0,0))):
    return ret

  if ((my_bunretu == 0) and (my_hand[0] >= 2) and (my_hand[1] == 0)):
    for i in range(my_hand[0] // 2 + 1):
      if (curt_turn == 0):
        ret.append([next_turn, [1,(my_hand[0]-i,i)], [op_bunretu, op_hand]])
      else:
        ret.append([next_turn, [op_bunretu, op_hand], [1,(my_hand[0]-i,i)]])

  next_op_hand_set = set()
  for i in [[0,0],[0,1],[1,0],[1,1]]:
    if (my_hand[i[1]] == 0):
      continue

    tmp0 = (op_hand[i[0]] + my_hand[i[1]]) % MAX_FINGER_NUM
    tmp1 = op_hand[1-i[0]]
    if (tmp0 >= tmp1):
      next_op_hand_set.add((tmp0, tmp1))
    else:
      next_op_hand_set.add((tmp1, tmp0))

  if ((0,0) in next_op_hand_set):
    if (curt_turn == 0):
      return [[next_turn, [my_bunretu, my_hand], [op_bunretu, (0,0)]]]
    else:
      return [[next_turn, [op_bunretu, (0,0)], [my_bunretu, my_hand]]]

  for next_op_hand in next_op_hand_set:
    if (curt_turn == 0):
      ret.append([next_turn, [my_bunretu, my_hand], [op_bunretu, next_op_hand]])
    else:
      ret.append([next_turn, [op_bunretu, next_op_hand], [my_bunretu, my_hand]])

  return ret


if __name__ == '__main__':
  hand_list = [(x,y) for x in range(0,MAX_FINGER_NUM) for y in range(0,x+1)]
  player_list = [[bunretu, hand] for bunretu in [0,1] for hand in hand_list]
  state_list = [[teban,p0,p1] for teban in [0,1] for p0 in player_list for p1 in player_list]
  init_state = [0, [0,(1,1)], [0,(1,1)]]

  print("digraph G {")
  print("node [shape = box];")
  print("rankdir=BT")

  d = {}
  memo = {}
  for i in range(len(state_list)):
    s_hash = str(state_list[i])
    d[s_hash] = i
    memo[s_hash] = 0

  rest_list = [init_state]
  while (len(rest_list) > 0):
    s = rest_list.pop(0)
    if (memo[str(s)] == 1):
      continue

    memo[str(s)] = 1
    for ns in get_next_state_list(s):
      print(str(d[str(s)]) + ' -> ' + str(d[str(ns)]))
      rest_list.append(ns)

  for s in state_list:
    if (memo[str(s)] == 1):
      s1_str = str(s[1]).translate(str.maketrans({' ':'', ',':'', '[':'', ']':'', '(':'', ')':''}))
      s2_str = str(s[2]).translate(str.maketrans({' ':'', ',':'', '[':'', ']':'', '(':'', ')':''}))
      label = s1_str + '-' + s2_str
      if (s[0] == 0):
        print(str(d[str(s)]) + ' [label="' + label + '", color=red];')
      if (s[0] == 1):
        print(str(d[str(s)]) + ' [label="' + label + '", color=blue];')

  print("}")
