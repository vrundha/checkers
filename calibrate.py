from homework import CheckerSolver, BoardEnv
import time
import math
import json

# white's turn to play

input_start = [
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
    ['.', '.', '.', '.', '.', 'b', '.', 'b'],
    ['b', '.', 'b', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', 'w', '.', 'w'],
    ['w', '.', 'w', '.', '.', '.', '.', '.'],
    ['.', 'w', '.', 'w', '.', 'w', '.', 'w'],
    ['w', '.', 'w', '.', 'w', '.', 'w', '.']]



input_mid = [

    ['.', 'W', '.', 'W', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'b', '.'],
    ['.', '.', '.', '.', '.', 'b', '.', 'b'],
    ['.', '.', 'b', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'b', '.', '.', '.', 'w'],
    ['b', '.', '.', '.', 'b', '.', 'w', '.'],
    ['.', 'w', '.', '.', '.', '.', '.', 'w'],
    ['.', '.', 'w', '.', '.', '.', '.', '.']]

input_end = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'W', '.', 'W', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'W', '.', '.', '.'],
    ['.', 'B', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', 'B', '.', 'B', '.', '.', '.']
]

ti = {"start": {}, "mid": {}, "end": {}}

c = CheckerSolver.from_array(input_start, BoardEnv.WHITE)
for i in range(3, 6):
    start = time.time()
    _, _, _ = c.alpha_beta(depth=i, is_calibrating=True)
    ti["start"][i] = time.time()-start


c = CheckerSolver.from_array(input_mid, BoardEnv.WHITE)
for i in range(4, 9):
    start = time.time()
    _, _, _ = c.alpha_beta(depth=i, is_calibrating=True)
    ti["mid"][i] = time.time()-start


c = CheckerSolver.from_array(input_end, BoardEnv.WHITE)
for i in range(4, 9):
    start = time.time()
    _, _, _ = c.alpha_beta(depth=i, is_calibrating=True)
    ti["end"][i] = time.time()-start


with open("calibration.txt", "w") as calibrate_f:
    json.dump(ti, calibrate_f, indent=2)


