from Wing_Calculator import chord
#aileron design

print(chord)

c_l_a = 0.1
tau = 0.1
S_ref = 1
b = 10

c_l_da = 2 * c_l_a * tau / (S_ref * b) * 1
