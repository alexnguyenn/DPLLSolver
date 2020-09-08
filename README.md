# DPLLSolver
Implementation of the **Davis–Putnam–Logemann–Loveland (DPLL)** algorithm for solving CNF-SAT problems. This project is a part of **CMPT 310: Artificial Intelligence Survey** (Simon Fraser University, Fall 2019) taught by Maxwell Libbrecht.

## Implementation
The program takes in a CNF formula in **DIMACS CNF file format** (read more [here](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html#:~:text=CNF%20is%20a%20data%20directory,example%20of%20the%20satisfiability%20problem.)). It will return `UNSAT` if the formula is unsatisfiable and `SAT` if it is satisfiable. A list of true literals from the solution can also be printed using the launch option `-v`.

An outline of the DPLL algorithm can be found [here](https://en.wikipedia.org/wiki/DPLL_algorithm). Tactics used to improve running time of the algorithm included removing redundant clauses and literals, applying variable selection heuristic and using efficient data structures. 

## Usage
To run the program use the following command:

`python DPLLsat.py -i <inputCNFfile>` 

or

`python DPLLsat.py -i <inputCNFfile> -v `

if you wish to see the solution. `./test_cases` provides some test cases with varying difficulties. Extra benchmark problems can be founds [here](https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html).
