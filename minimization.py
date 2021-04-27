import json
import csv
from numpy import *

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

Resultat = ""
init = int(initial_state[0])
#DFA Minimization using Myphill-Nerode Theorem
#Nfs contain the no final states
Nfs = [set_of_states[a] for a in range(0, len(set_of_states)) if set_of_states[a] not in set_of_final_state] #set of NFS
Matrix = []
A = []
for i in range (0,len(set_of_states)):
        for j in range(0, len(set_of_states)):
            if (((set_of_states[i] in Nfs) and (set_of_states[j] in set_of_final_state)) or ((set_of_states[j] in Nfs) and (set_of_states[i] in set_of_final_state))):
                A.append('X')
            else:
                A.append('E')

        Matrix.append(A)
        del(A)
        A = []

#1 st step Draw a table for all pairs of states (Qi, Qj) not necessarily connected directly [All are unmarked initially]
for i in range(0,len(set_of_states)):
    for j in range(0, len(set_of_states)):
        if (j>=i):
            Matrix[i][j]='G'

# 2nd step Consider every state pair (Qi, Qj) in the DFA where Qi ∈ F and Qj ∉ F or vice versa and mark them with "X"
for i in range(0,len(set_of_states)):
    for j in range(0, len(set_of_states)):
        for k in range(0, len(set_of_states)):
            if ((Matrix[j][i] == 'X') and (Matrix[k][j] == 'X')):
                Matrix[k][i]='X'


#3rd step If there is an unmarked pair (Qi, Qj), mark it if the pair {δ (Qi, A), δ (Qi, A)} is marked for some input alphabet.
#G means unimportant
#E is Empty
S1=[]
S2=[]
tabX=[]
for i in range(1,len(set_of_states)):
    for j in range(0, i):
        if(j<i):
            if ((Matrix[i][j] == 'E')):
                if (((str(i) in set_of_final_state) or (str(j) in set_of_final_state)) and (str(i) not in S1) and (str(j) not in S1)):
                    S1.append(str(j))
                    S1.append(str(i))
                elif (((str(i) in Nfs) or (str(j) in Nfs) and (str(i) not in S2)) and (str(j) not in S2)):
                    S2.append(str(j))
                    S2.append(str(i))
            else:
                if (((str(j) not in S1) and (str(j) not in S2))and (str(j) not in tabX)):
                    tabX.append(str(j))
                if(((str(i) not in S1) and (str(i) not in S2)) and (str(i) not in tabX)):
                    tabX.append(str(i))


#4th step
s1=""
s2=""
A= []
for a in range(0, len(S1)):
    s1 = s1 + str(S1[a])
for a in range(0, len(S2)):
    s2 = s2 + str(S2[a])

new_set_of_states = []
new_set_of_final_state = []
new_initial_state = []
if (initial_state in S2):
    new_initial_state.append(s2)
else:
    new_initial_state.append(initial_state)

for i in range(0,len(set_of_final_state)):
    if (set_of_final_state[i] in s1):
        new_set_of_final_state.append(s1)
    if (set_of_final_state[i] not in s1):
        new_set_of_final_state.append(set_of_final_state[i])
print('----------------------------------------------------------------------------')
print('The new set of final states')
print(new_set_of_final_state)
tabX_str=''
if (s2 != ''):
    new_set_of_states.append(s2)

for i in range(0, len(tabX)):
    new_set_of_states.append(tabX[i])

if (s1 != ''):
    new_set_of_states.append(s1)

print('new_set_of_states : ')
print(new_set_of_states)

del(A)
A = []
New_transition = []
if (len(S2) != 0):
    for i in range(0, len(set_of_alphabet)):
        for j in range(0, len(S2)):
            if ((Mat[int(S2[j])][i] in S1) and (j==0)):
                    A.append(s1)
            elif ((Mat[int(S2[j])][i] in S1) and(j != 0)):
                    A[i] = s2
            elif ((Mat[int(S2[j])][i] in S2) and (j==0)):
                    A.append(s2)
            elif ((Mat[int(S2[j])][i] in S2) and(j != 0)):
                    A[i] = s2
            else:
                if (j == 0):
                    A.append(Mat[int(S2[j])][i])
                else:
                    A[i] =Mat[int(S2[j])][i]

    New_transition.append(A)

del(A)
A = []


for i in range(0,len(tabX)):
    for j in range(0, len(set_of_alphabet)):
        A.append(Mat[int(tabX[i])][j])
    New_transition.append(A)
    del (A)
    A = []

if (len(S1) != 0):
    for i in range(0, len(set_of_alphabet)):
        for j in range(0, len(S1)):
            if ((Mat[int(S1[j])][i] in S1) and (j == 0)):
                A.append(s1)
            elif ((Mat[int(S1[j])][i] in S1) and (j != 0)):
                A[i] = s2
            elif ((Mat[int(S1[j])][i] in S2) and (j == 0)):
                A.append(s2)
            elif ((Mat[int(S1[j])][i] in S2) and (j != 0)):
                A[i] = s2
            else:
                if (j == 0):
                    A.append(Mat[int(S1[j])][i])
                else:
                    A[i] = Mat[int(S1[j])][i]
    New_transition.append(A)




print('New_transition : ')
print(New_transition)


min_Dfa = {
    "states": [

        {
            "set of states": new_set_of_states,
            "set of alphabet": set_of_alphabet,
            "initial state": new_initial_state,
            "set of final state": new_set_of_final_state
        },
    ],


}




def transitionfuction(i):
    trans = {
        "transition function": [

        {
            "current state": new_set_of_states[i],
            "value": set_of_alphabet,
            "Target state": New_transition[i]
        },

    ],
    }
    json.dump(trans, json_file)
    print(trans)

with open('min_Dfa.json', 'w') as json_file:
    json.dump(min_Dfa, json_file)

    for i in range (0 ,len(New_transition)):
        transitionfuction(i)
