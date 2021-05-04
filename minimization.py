import json
import csv
from numpy import *

class minimizations:
    '''

    Draw a table for all pairs of states (P,Q)
    Mark all pairs where P is a final state and Q is not a final state.
    If there are any unmarked pairs such that [delta(P,x), delta(Q,x)] is marked, then mark (P,Q)
    Combine all the unmarked pairs and make them a single state in the minimized DFA.
    '''
    def __init__(self, dFa):
        dfa, Mat = dFa
        Matrix = []
        # Nfs contain the no final states
        Nfs = [dfa['states'][a] for a in range(0, len(dfa['states'])) if
               dfa['states'][a] not in dfa['accepting_states']]  # set of NFS
        S1 = []
        S2 = []
        tabX = []

    def step_1(self):
        #1st step
        init = int(self.dfa['starting_state'][0])
        A = []
        # Draw a table for all pairs of states (Qi, Qj)
        #if (Qi, Qj) connected then contains 'X'
        #if (Qi, Qj) not connected then contains 'E'
        for s1 in self.dfa['states']:
            for s2 in self.dfa['states']:
                if (((s1 in self.Nfs) and (s2 in self.dfa['accepting_states'])) or ((s2 in self.Nfs) and (s1 in self.dfa['accepting_states']))):
                    A.append('X')
                else:
                    A.append('E')

            self.Matrix.append(A)
            del (A)
        #if (Qi, Qj) not necessary then contains 'G'
        A = []
        for i in range(0, len(self.dfa['states'])):
            for j in range(0, len(self.dfa['states'])):
                if (j >= i):
                    self.Matrix[i][j] = 'G'
    def step_2(self):
        self.step_1()
        # 2nd step Consider every state pair (Qi, Qj) in the DFA where Qi ∈ F and Qj ∉ F or vice versa and mark them with "X"
        for i in range(0, len(self.dfa['states'])):
            for j in range(0, len(self.dfa['states'])):
                for k in range(0, len(self.dfa['states'])):
                    if ((self.Matrix[j][i] == 'X') and (self.Matrix[k][j] == 'X')):
                        self.Matrix[k][i] = 'X'
    def step_3(self):
        self.step_2()
        # 3rd step If there is an unmarked pair (Qi, Qj), mark it if the pair {δ (Qi, A), δ (Qi, A)} is marked for some input alphabet.
        # 'G' : unimportant
        # 'E' : Empty
        for i in range(1, len(self.dfa['states'])):
            for j in range(0, i):
                if (j < i):
                    if ((self.Matrix[i][j] == 'E')):
                        if (((str(i) in self.dfa['accepting_states']) or (str(j) in self.dfa['accepting_states'])) and (str(i) not in self.S1) and (
                                str(j) not in self.S1)):
                            self.S1.append(str(j))
                            self.S1.append(str(i))
                        elif (((str(i) in self.Nfs) or (str(j) in self.Nfs) and (str(i) not in self.S2)) and (str(j) not in self.S2)):
                            self.S2.append(str(j))
                            self.S2.append(str(i))
                    else:
                        if (((str(j) not in self.S1) and (str(j) not in self.S2)) and (str(j) not in self.tabX)):
                            self.tabX.append(str(j))
                        if (((str(i) not in self.S1) and (str(i) not in self.S2)) and (str(i) not in self.tabX)):
                            self.tabX.append(str(i))
    def step_4(self):
        self.step_3()
        # 4th step
        s1 = ""
        s2 = ""
        A = []
        #Creat names for the new states
        for a in range(0, len(self.S1)):
            s1 = s1 + str(self.S1[a])
        for a in range(0, len(self.S2)):
            s2 = s2 + str(self.S2[a])

        newsetofstates = []
        newsetoffinalstate = []
        newinitialstate = []
        if (self.dfa['starting_state'] in self.S2):
            newinitialstate.append(s2)
        else:
            newinitialstate.append(self.dfa['starting_state'])
        for i in range(0, len(self.dfa['accepting_states'])):
            if (self.dfa['accepting_states'][i] in s1):
                newsetoffinalstate.append(s1)
            if (self.dfa['accepting_states'][i] not in s1):
                newsetoffinalstate.append(self.dfa['accepting_states'][i])
        tabX_str = ''
        #creat the new states
        if (s2 != ''): #initial states
            newsetofstates.append(s2)
        for i in range(0, len(self.tabX)): # normal states
            newsetofstates.append(self.tabX[i])
        if (s1 != ''): #final states
            newsetofstates.append(s1)
        del (A)
        A = []
        #Creat a table of transition
        New_transition = []
        if (len(self.S2) != 0):
            for i in range(0, len(self.dfa['alphabet'])):
                for j in range(0, len(self.S2)):
                    if ((self.Mat[int(self.S2[j])][i] in self.S1) and (j == 0)):
                        A.append(s1)
                    elif ((self.Mat[int(self.S2[j])][i] in self.S1) and (j != 0)):
                        A[i] = s2
                    elif ((self.Mat[int(self.S2[j])][i] in self.S2) and (j == 0)):
                        A.append(s2)
                    elif ((self.Mat[int(self.S2[j])][i] in self.S2) and (j != 0)):
                        A[i] = s2
                    else:
                        if (j == 0):
                            A.append(self.Mat[int(self.S2[j])][i])
                        else:
                            A[i] = self.Mat[int(self.S2[j])][i]

            New_transition.append(A)

        del (A)
        A = []

        for i in range(0, len(self.tabX)):
            for j in range(0, len(self.dfa['alphabet'])):
                A.append(self.Mat[int(self.tabX[i])][j])
            New_transition.append(A)
            del (A)
            A = []

        if (len(self.S1) != 0):
            for i in range(0, len(self.dfa['alphabet'])):
                for j in range(0, len(self.S1)):
                    if ((self.Mat[int(self.S1[j])][i] in self.S1) and (j == 0)):
                        A.append(s1)
                    elif ((self.Mat[int(self.S1[j])][i] in self.S1) and (j != 0)):
                        A[i] = s2
                    elif ((self.Mat[int(self.S1[j])][i] in self.S2) and (j == 0)):
                        A.append(s2)
                    elif ((self.Mat[int(self.S1[j])][i] in self.S2) and (j != 0)):
                        A[i] = s2
                    else:
                        if (j == 0):
                            A.append(self.Mat[int(self.S1[j])][i])
                        else:
                            A[i] = self.Mat[int(self.S1[j])][i]
            New_transition.append(A)
        dfa = {
            "states": newsetofstates,
            "alphabet": self.dfa['alphabet'],
            "starting_state": newinitialstate,
            "accepting_states": newsetoffinalstate
        }
        return dfa,New_transition

