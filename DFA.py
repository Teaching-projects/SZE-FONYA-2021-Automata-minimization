import json
import csv
from numpy import *


with open("file.json", "r") as read_file:
    data = json.load(read_file)
    for p in data['states']:
        set_of_states = p['set of states'].split(',')
        print('set of states ' )
        print(set_of_states)
        set_of_alphabet = p['set of alphabet'].split(',')
        print('set of alphabet ' )
        print( set_of_alphabet)
        initial_state = p['initial state'].split(',')
        print('initial state ' )
        print(initial_state)
        set_of_final_state = p['set of final state'].split(',')
        print('set of final state ')
        print(set_of_final_state)
    Mat = []
    for p in data['transition function']:
        Mat.append(p['Target state'])

Resultat = ""
init = int(initial_state[0])
inp = input('The input: ')
for i in range(0,len(inp)):
    for j in range(0, len(set_of_alphabet)):
        if (set_of_alphabet[j] == inp[i]):
            Resultat= Resultat + str(set_of_alphabet[j])
            init = int(Mat[init][j])
            break



if ((Resultat == inp)and (str(init) in set_of_final_state)):
    print('Correct')
else:
    print('incorrect')

