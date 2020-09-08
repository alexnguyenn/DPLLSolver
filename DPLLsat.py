import sys, getopt
import copy
import random
import time
import numpy as np
from collections import Counter
sys.setrecursionlimit(10000)

class SatInstance:
    def __init__(self):
        pass

    def from_file(self, inputfile):
        # Read DIMACS CNF file format
        # (Note: code provided by instructor)

        # instance.VARS goes 1 to N in a dictionary
        # instance.clauses return array contains every clause [[4,-5, 6],[9,1,-8],...]
        # Note: vars = symbols

        self.clauses = list()
        self.VARS = set()
        self.p = 0
        self.cnf = 0
        with open(inputfile, "r") as input_file:
            self.clauses.append(list())
            maxvar = 0
            for line in input_file:
                tokens = line.split()
                if len(tokens) != 0 and tokens[0] not in ("p", "c"):
                    for tok in tokens:
                        lit = int(tok)
                        maxvar = max(maxvar, abs(lit))
                        if lit == 0:
                            self.clauses.append(list())
                        else:
                            self.clauses[-1].append(lit)
                if tokens[0] == "p":
                    self.p = int(tokens[2])
                    self.cnf = int(tokens[3])
            assert len(self.clauses[-1]) == 0
            self.clauses.pop()
            if (maxvar > self.p):
                print("Non-standard CNF encoding!")
                sys.exit(5)
        # Variables are numbered from 1 to p
        for i in range(1, self.p + 1):
            self.VARS.add(i)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s


def main(argv):
    # Main function
    # (Note: Code provided by instructor)

    inputfile = ''
    verbosity = False
    inputflag = False
    try:
        opts, args = getopt.getopt(argv, "hi:v", ["ifile="])
    except getopt.GetoptError:
        print('DPLLsat.py -i <inputCNFfile> [-v] ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('DPLLsat.py -i <inputCNFfile> [-v]')
            sys.exit()
        
        # -v sets the verbosity of informational output
        # (set to true for output veriable assignments, defaults to false)
        
        elif opt == '-v':
            verbosity = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            inputflag = True
    
    if inputflag:
        instance = SatInstance()
        instance.from_file(inputfile)
        # start_time = time.time()
        solve_dpll(instance, verbosity)
        # print("--- %s seconds ---" % (time.time() - start_time))

    else:
        print("You must have an input file!")
        print('DPLLsat.py -i <inputCNFfile> [-v]')


def solve_dpll(instance, verbosity):
    clauses = instance.clauses
    variables = instance.VARS
    model = {}
    
    # Start DPLL
    ret = dpll_recur(clauses, variables, model)
    
    # Print results
    if not ret: print("UNSAT")
    else:
        print("SAT")
        if verbosity:
            arr = []
            for P in model:
                if model[P]: arr.append(P)
            arr.sort()
            print(arr)

def updateClause(clauses, P):
    # Remove satisfied clauses, remove literals from clauses that do not satisfy
    # P must be True

    new = []
    if clauses == -1:
        return -1
    
    for c in clauses:
        if P in c: continue
        if -P in c:
            arr = [x for x in c if x != -P]
            # If empty clause exists -> model does not work
            if not arr: return -1
            new.append(arr)
        else: new.append(c)
    return new

def findPure(clauses):
    # Return first found pure literal, None if not found any
    P = None
    
    # Extract set of literals (both polarities) from clauses
    literals = {s for c in clauses for s in c}

    for l in literals:
        if -l not in literals:
            P = l
            break
    return P

def findUnit(clauses):
    # Return the first found unit clause, None if not found any
    P = None
    for c in clauses:
        if len(c) == 1:
            P = c[0]
            break
    return P

def degreeHeuristic(clauses):
    # Return most frequent element in the remaning clauses
    # Using Counter() for efficiency sake
    data = Counter([abs(x) for c in clauses for x in c])
    return data.most_common(1)[0][0]

def dpll_recur(clauses, symbols, model):
    # DPLL implementation
    if not clauses:
        return True
    if clauses == -1:
        return False

    tmp_symbols = copy.copy(symbols)
    
    # Pure literal elmination
    P = findPure(clauses)
    if P:
        model.update({abs(P): P > 0})
        tmp_symbols.remove(abs(P))
        return dpll_recur(updateClause(clauses, P), tmp_symbols, model)
    
    # Unit propagation
    P = findUnit(clauses) 
    if P:
        model.update({abs(P): P > 0})
        tmp_symbols.remove(abs(P))
        return dpll_recur(updateClause(clauses, P), tmp_symbols, model)

    # Backtracking
    P = degreeHeuristic(clauses)
    tmp_symbols.remove(P)
    model.update({P: True})
    ret = dpll_recur(updateClause(clauses, P), tmp_symbols, model)
    if not ret:
        model.update({P: False})
        ret =  dpll_recur(updateClause(clauses, -P), tmp_symbols, model)
    return ret

    ###########################################

if __name__ == "__main__":
    main(sys.argv[1:])