# Classical Planner

## Tutorial
In order to run the solver, run:

```python
python -B -m pddl_parser.planner domain\path problem\path
```

## Parser

   To parse the problems initially, we relied on a pre-existing parser ([link](https://github.com/pucrs-automated-planning/pddl-parser))limited to handling conventional domain and problem descriptions, lacking support for conditional effects, disjunctive preconditions, existential, or universal conditions. With this parser, we conducted benchmarking of our planners using various heuristic functions and search algorithms.

For scenarios involving more intricate features, we employed a general-purpose parser from the PDDL library capable of accommodating these complex requirements.

## Research Algorithm Benchmarking

We utilized three different research algorithms to find the solution, described in the following lines:

1. **In-depth search**: In each state, we store all the possible actions and apply the first one. If there are no more possible actions and the objective is not achieved, we backtrack and try another action until we find the solution.

2. **A***: In each iteration, we select the node with the lowest estimated total cost. For this, we consider the cost function as \( f(n) = g(n) + h(n) \), where \( g(n) \) represents the estimated cost from the initial state to the current state (calculated by the depth of the search tree), and \( h(n) \) is the heuristic, described below.

3. **Iterative Deepening A***: The second approach is a variation of A* where we calculate the initial cost of the state \( T \) and add to the set of possible actions only those actions whose cost is lower than \( T \). If no action is possible, we return all possible actions regardless of \( T \).

To change the strategy of the research algorithm, modify the ```pddl-parser/planner.py``` file. In line 143, specify the strategy you wish to adopt.

## Heuristics Benchmarking

We conducted a benchmarking study to evaluate the performance of different heuristics in solving planning problems. Four distinct heuristics were tested, each offering unique insights into the problem space.
To choose a heuristics to implement in the research algorithm, call the respective function from [planner.py]([https://github.com/user/repository/blob/branch/path/to/file](https://github.com/Salahidine2002/Plannif_auto/blob/main/pddl_parser/planner.py))
, in the ```heuristic_cost ``` variable.

1. **Simple Heuristic (`h`)**:

   This straightforward heuristic calculates a heuristic value based on the difference between the current state and the goal state. It assesses the presence of positive goals and the absence of negative goals in the current state. The heuristic value is incremented for each unsatisfied positive goal and each present negative goal. Despite its simplicity, this heuristic offers a basic estimate of the distance to the goal state.  
   We give the possibility to attribute different weights to each predicate of the domain, since we thought that some have more importance than other, and unsatisfying them will led to bigger price.

2. **Planning Graph Level Sum Heuristic (`h_pg_levelsum`)**:

   The Planning Graph Level Sum heuristic leverages a planning graph representation of the problem state space to estimate the sum of the number of actions required to satisfy each individual goal condition. It analyzes the planning graph to determine the level at which each goal condition is achieved and sums up these levels to provide an overall estimate of the distance to the goal state. This heuristic is based on the approach outlined in Russell-Norvig (3rd Edition).

3. **Planning Graph Max Level Heuristic (`h_pg_maxlevel`)**:

   In this heuristic, a planning graph representation is used to estimate the maximum level cost among all individual goal literals. The level cost corresponds to the first level at which a goal literal appears in the planning graph. By identifying the highest level at which any goal appears, this heuristic provides a conservative estimate of the distance to the goal state. This approach is inspired by Russell-Norvig (3rd Edition).


5. **Planning Graph Set Level Heuristic (`h_pg_setlevel`)**:

   The Planning Graph Set Level heuristic utilizes a planning graph to estimate the level cost required to achieve all goal literals without any mutual exclusions. It searches for a level where all goals are present in the planning graph and ensures that no pair of goal literals is mutually exclusive in that layer. This heuristic offers a nuanced estimate of the distance to the goal state by considering the interplay between different goal conditions in the planning graph. The methodology for this heuristic is derived from Russell-Norvig (3rd Edition).

## Further investigations : Symbolic Reasoning & Search Algorithms : 

   Handling complex features like conditional effects in planning algorithms requires more sophisticated techniques than simple state-space search with heuristics. In this part we investigated the possibility of combining
symbolic resoning with our planner to adapt them to the new complexity level. Instead of directly applying actions to the current state, we tried use symbolic reasoning to compute the effects of actions under different conditions. This involves reasoning about the effects of actions based on the current state and the conditions specified in the action's preconditions formulated as axioms in a knowledge base, then inferring them as knowledge base requests. For this part we experimented using pddl-solver library. 
