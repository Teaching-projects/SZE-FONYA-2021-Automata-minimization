import json
import csv
import time
from graphviz import Digraph
from numpy import *
import minimization



def load_DFA(file):
    with open(file, "r") as read_file:
        data = json.load(read_file)
        A = []
        Mat = []
        set_of_states, set_of_alphabet, initial_state, set_of_final_state = data['states'],data['alphabet'],data['starting_state'],data['accepting_states']
        prev_src = str(initial_state)
        current_src = str(initial_state)
        for p in data['transitions']:
            current_src = p['source']
            if (prev_src == current_src):
                A.append(p['destination'])
            else:
                Mat.append(A)
                prev_src = current_src
                del (A)
                A = []
                A.append(p['destination'])
            if (data['transitions'][len(data['transitions'])-1] == p):
                Mat.append(A)
                del (A)
                A = []
    del (A)
    return data,Mat
def test_word():
    file = ('file.json')
    data, Mat = load_DFA(file)
    set_of_states, set_of_alphabet, initial_state, set_of_final_state = data['states'],data['alphabet'],data['starting_state'],data['accepting_states']
    A = []
    Resultat = []
    init = int(initial_state[0])
    inp = input('The input: ')
    for i in range(0, len(inp)):
        for j in range(0, len(set_of_alphabet)):
            if (set_of_alphabet[j] == inp[i]):
                Resultat.append(set_of_alphabet[j])
                init = int(Mat[init][j])
                break

    if ((str(Resultat) == inp) and (str(init) in set_of_final_state)):
        return True
    else:
        return False


def save_DFA_to_file(dFa, filename):
    dfa, New_transition = dFa
    new_set_of_states, set_of_alphabet, new_initial_state, new_set_of_final_state = dfa['states'], dfa['alphabet'], dfa[
        'starting_state'], dfa['accepting_states']
    transitions = []
    for i in range(0, len(New_transition)):
        for j in range(0, len(set_of_alphabet)):
            transit = {"source": new_set_of_states[i], "symbol": set_of_alphabet[j],
                       "destination": New_transition[i][j]}
            transitions.append(transit)
    with open(filename+'.json', 'w') as json_file:
        min_Dfa = {
            "states": new_set_of_states,
            "alphabet": set_of_alphabet,
            "starting_state": new_initial_state,
            "accepting_states": new_set_of_final_state,
            "transitions": transitions
        }
        json.dump(min_Dfa, json_file)


"""
def minimization():
    file = ('file.json')
    data, Mat = load_DFA(file)
    set_of_states, set_of_alphabet, initial_state, set_of_final_state = data['states'], data['alphabet'], data[
        'starting_state'], data['accepting_states']

    init = int(initial_state[0])
    #DFA Minimization using Myphill-Nerode Theorem
    #Nfs contain the no final states
    Nfs = [set_of_states[a] for a in range(0, len(set_of_states)) if set_of_states[a] not in set_of_final_state] #set of NFS
    Matrix = []
    A = []
    for s1 in set_of_states:
            for s2 in set_of_states:
                if (((s1 in Nfs) and (s2 in set_of_final_state)) or ((s2 in Nfs) and (s1 in set_of_final_state))):
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
    tabX_str=''
    if (s2 != ''):
        new_set_of_states.append(s2)

    for i in range(0, len(tabX)):
        new_set_of_states.append(tabX[i])

    if (s1 != ''):
        new_set_of_states.append(s1)

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
    dfa = {
        "states" : new_set_of_states,
        "alphabet" : set_of_alphabet,
        "starting_state" : new_initial_state,
        "accepting_states" : new_set_of_final_state
          }
    return dfa,New_transition
"""
def graph(file):
    data, Mat = load_DFA(file)
    set_of_states, set_of_alphabet, initial_state, set_of_final_state = data['states'], data['alphabet'], data[
        'starting_state'], data['accepting_states']
    print(Mat)

    dot = Digraph('DFA')
    for i in range(0, len(set_of_states)):
        dot.node(set_of_states[i], 'state ' + '(' + str(i) + ')')
        dot.edges([str(i) + Mat[i][0], str(i) + Mat[i][1]])
    print(dot)
    dot.render('test-output/round-table.gv', view=True)





file = "file.json"
min1 = minimization.minimizations(load_DFA(file))
while(True):
    print("1: read input and test it from file.json")
    print("2: minimize DFA from file.json to min_Dfa.json" )
    print("3: Graph DFA from file.json \n")
    inp = input("give me an input \n")
    if(inp == '1'):
        if (test_word()):
            print('Correct')
        else:
            print('incorrect')
    if(inp == '2'):
        save_DFA_to_file(min1.step_4(),'min_Dfa')
        print(min1.step_4())
    if(inp == '3'):
        graph(file)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    print('q : quitting button ')
    if inp == 'q':
        break
