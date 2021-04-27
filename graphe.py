import json
import csv
from numpy import *
import sys
from graphviz import Digraph
import graphviz
#reading the file
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

print(Mat[0])
dot = Digraph('DFA')
for i in range(0,len(set_of_states)):
    dot.node(set_of_states[i], 'state ' + '('+str(i)+')')
    dot.edges( [str(i)+ Mat[i][0] , str(i)+Mat[i][1]]  )

print(dot)
dot.render('test-output/round-table.gv', view=True)

