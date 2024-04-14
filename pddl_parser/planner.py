#!/usr/bin/env python
# Four spaces as indentation [no tabs]

# This file is part of PDDL Parser, available at <https://github.com/pucrs-automated-planning/pddl-parser>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from pddl_parser.PDDL import PDDL_Parser
from pddl_parser.heuristic import h
from .planning_problem import BasePlanningProblem
import sys, time


class Planner:
    # -----------------------------------------------
    # Solve
    # -----------------------------------------------

    def solve(self, domain, problem):
        # Parser
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        # Parsed data
        state = parser.state
        goal_pos = parser.positive_goals
        goal_not = parser.negative_goals
        # Do nothing because is applicable
        if self.applicable(state, goal_pos, goal_not):
            return [] 
        # Grounding process
        ground_actions = []
        print("Objects", parser.objects)
        print("Types", parser.types)
        # Get all the actions as posible
        for action in parser.actions:
            for act in action.groundify(parser.objects, parser.types):
                ground_actions.append(act)
        # Search
        visited = set([state])
        fringe = [state, None]
        while fringe:
            state = fringe.pop(0)
            plan = fringe.pop(0)
            for act in ground_actions:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions): # check if this action is applicable
                    new_state = self.apply(state, act.add_effects, act.del_effects) # apply the action if is available and change the state
                    if new_state not in visited:
                        if self.applicable(new_state, goal_pos, goal_not): # check if the new state is the goal
                            full_plan = [act]
                            while plan:
                                act, plan = plan
                                full_plan.insert(0, act) # insert the action in the plan
                            return full_plan
                        visited.add(new_state)       # add the new state to the visited states
                        fringe.append(new_state)     # add the new state to the fringe
                        fringe.append((act, plan))   # add the action and the plan to the fringe
        return None
    
    def solver_research_heuristic(self, domain, problem):
        """A* search is best-first graph search with f(n) = g(n)+h(n)."""
        print("\n", "#"*7,"Solver with research algorithm and heuristic", "#"*7, "\n")
        # Parser
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        # Parsed data
        state = parser.state
        ini_state = state
        print(state)
        goal_pos = parser.positive_goals
        goal_not = parser.negative_goals
        # Do nothing because is applicable
        if self.applicable(state, goal_pos, goal_not):
            return [] 
        # Grounding process
        ground_actions = []
        print("Objects", parser.objects)
        print("Types", parser.types)
        # Get all the actions as posible
        for action in parser.actions:
            for act in action.groundify(parser.objects, parser.types):
                ground_actions.append(act)
        # Search
        visited = set([state])
        fringe = [(state, [], 0)]  # Include path_cost in the fringe tuple

        while fringe:
            state, plan, path_cost = fringe.pop(0)  # Unpack path_cost
            aplicable_actions = []
            for act in ground_actions:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    # Calculate the total cost for reaching this new state
                    new_cost = path_cost + 1  # Increment path cost as you dive deeper
                    planning_problem = BasePlanningProblem(ini_state, state, goal_pos, goal_not, act, path_cost)
                    # Choose the heuristic you want to use, h, h_pg_setlevel, h_pg_levelsum or h_pg_maxlevel 
                    heuristic_cost = planning_problem.h_pg_maxlevel()
                    #heuristic_cost = h(state, goal_pos, goal_not)
                    cost = new_cost + heuristic_cost  # g(n) + h(n)
                    aplicable_actions.append((act, cost))

            # Sort the list of aplicable actions by cost
            aplicable_actions.sort(key=lambda x: x[1])

            for act, cost in aplicable_actions:
                new_state = self.apply(state, act.add_effects, act.del_effects)
                if new_state not in visited:
                    if self.applicable(new_state, goal_pos, goal_not):
                        full_plan = plan + [act]
                        return full_plan, len(full_plan), path_cost  # Return path_cost as depth
                    visited.add(new_state)
                    fringe.append((new_state, plan + [act], path_cost + 1))  # Update path_cost here

        return None
    
    def solver_research_heuristic_IDA(self, domain, problem):
        """A* search is best-first graph search with f(n) = g(n)+h(n)."""
        print("\n", "#"*7,"Solver with research algorithm and heuristic", "#"*7, "\n")
        # Parser
        parser = PDDL_Parser()
        parser.parse_domain(domain)
        parser.parse_problem(problem)
        # Parsed data
        state = parser.state
        print(state)
        goal_pos = parser.positive_goals
        goal_not = parser.negative_goals
        # Do nothing because is applicable
        if self.applicable(state, goal_pos, goal_not):
            return [] 
        # Grounding process
        ground_actions = []
        print("Objects", parser.objects)
        print("Types", parser.types)
        # Get all the actions as posible
        for action in parser.actions:
            for act in action.groundify(parser.objects, parser.types):
                ground_actions.append(act)
        # Search
        visited = set([state])
        fringe = [(state, [], 0)]  # Include path_cost in the fringe tuple

        # Define T value, we asume g(n) = 0
        T = 2**64
        
        while fringe:
            state, plan, path_cost = fringe.pop(0)  # Unpack path_cost
            aplicable_actions = []
            aplicable_actions_T = []
            for act in ground_actions:
                if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
                    # Calculate the total cost for reaching this new state
                    new_cost = path_cost + 1  # Increment path cost as you dive deeper
                    cost = new_cost + h(state, goal_pos, goal_not)  # g(n) + h(n)
                    if cost <= T:
                        aplicable_actions_T.append((act, cost))
                    aplicable_actions.append((act, cost))

            # Redefine T value if there is aplicable actions
            if aplicable_actions_T:
                T = aplicable_actions_T[0][1]
                aplicable_actions = aplicable_actions_T.copy()
            
            # Sort the list of aplicable actions by cost
            aplicable_actions.sort(key=lambda x: x[1])

            for act, cost in aplicable_actions:
                new_state = self.apply(state, act.add_effects, act.del_effects)
                if new_state not in visited:
                    if self.applicable(new_state, goal_pos, goal_not):
                        full_plan = plan + [act]
                        return full_plan, len(full_plan), path_cost  # Return path_cost as depth
                    visited.add(new_state)
                    fringe.append((new_state, plan + [act], path_cost + 1))  # Update path_cost here

        return None


    # -----------------------------------------------
    # Applicable
    # -----------------------------------------------

    def applicable(self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)

    # -----------------------------------------------
    # Apply
    # -----------------------------------------------

    def apply(self, state, positive, negative):
        return state.difference(negative).union(positive)


# -----------------------------------------------
# Main
# -----------------------------------------------
def main(domain, problem, verbose=False):
    start_time = time.time()
    planner = Planner()
    plan, steps, path_cost = planner.solver_research_heuristic(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    print('Steps: ' + str(steps))
    print('path_cost: ' +str(path_cost))
    if plan is not None:
        print('plan:')
        for act in plan:
            print(act if verbose else act.name + ' ' + ' '.join(act.parameters))
    else:
        print('No plan was found')

    # Créez un dictionnaire avec les résultats
    results = {
        'time': time.time() - start_time,
        'steps': steps,
        'path_cost': path_cost,
        'plan': [act if verbose else act.name + ' ' + ' '.join(act.parameters) for act in plan] if plan is not None else None
    }

    # Retournez les résultats
    return results

if __name__ == "__main__":
    import sys
    domain = sys.argv[1]
    problem = sys.argv[2]
    verbose = len(sys.argv) > 3 and sys.argv[3] == '-v'
    main(domain, problem, verbose)
