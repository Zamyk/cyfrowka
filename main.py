from automata.fa.dfa import DFA
from visual_automata.fa.dfa import VisualDFA
import logicmin

states = ["0000", "0100", "0001", "0101", "0010", "0110", "0011", "0111", "1000", "1100", "1001", "1101", "1010", "1110", "1011", "1111"]
# state: playing(1 bit) pressed(1 bit) song_number(2 bits)

possible_inputs = [format(i, '04b') for i in range(2 ** 4)]
# input: stop, play, next, previous

def move(number, v):
  i = int(number, 2)
  i += v

  if i < 0:
    i += 4

  if i > 3:
    i -= 4

  return format(i, '02b')

def process_input(input):
  stop, play, next, prev = tuple(input)

  if stop == "1" and play == "1":
    play = "0"

  if next == "1" and prev == "1":
    prev = "0"

  return stop + play + next + prev

def transition(state, processed):
  playing = state[0]
  pressed = state[1]
  number = state[2:4]

  if pressed == "0":
    # stop
    if processed[0] == "1":
      playing = "0"
      pressed = "1"

    # play
    if processed[1] == "1":
      playing = "1"
      pressed = "1"

    # next
    if processed[2] == "1":
      number = move(number, 1)
      pressed = "1"

    if processed[3] == "1":
      number = move(number, -1)
      pressed = "1"

  else:
    if input == "0000":
      pressed = "0"

  return playing + pressed + number

def get_transitions(state):
  ans = dict()
  for input in possible_inputs:
    processed = process_input(input)
    ans[input] = transition(state, processed)
  return ans


def draw_dfa():
    transitions = {
        state: get_transitions(state) for state in states
    }

    # Extract input symbols directly from the keys of the transitions
    input_symbols = set(trans for trans in transitions.values() for trans in trans.keys())

    dfa = VisualDFA(
        states=set(states),
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state="0000",
        final_states=set(),  # Define final states if any
    )
    print(dfa.table)

def get_logic_functions():
  tt = logicmin.TT(8, 4)
  for state in states:
    for input in possible_inputs:
      processed = process_input(input)
      t = transition(state, processed)
      tt.add(state + input, t)

  sols = tt.solve()
  print(sols.printN(xnames=["playing", "pressed", "numbe1", "number2", "stop", "play", "next", "previous"],ynames=["out_playing", "out_pressed", "out_number1", "out_number2"], info=True))  

draw_dfa()

print()
print()
print()
print()

get_logic_functions()
