from .planning_graph import PlanningGraph, Node
from .utils import encode_state, decode_state, make_relations_ng, FluentState

class BasePlanningProblem:
    def __init__(self, initial, state, goal_pos, goal_neg, result, g):
        self.possibleactions_state = {}
        self.expressions = make_relations_ng("expr", initial)
        self.pos = self.expressions
        self.neg = []
        self.initial = FluentState(self.pos, self.neg)

        self.goal_pos = make_relations_ng("expr", goal_pos)
        self.goal_neg = make_relations_ng("expr", goal_neg)
        self.goals = FluentState(self.goal_pos, self.goal_neg)
        self.state_map = list(sorted(self.initial.pos+self.initial.neg, key=str))

        self.result = result
        self.pos_precondition = make_relations_ng("expr", self.result.positive_preconditions)
        self.neg_precondition = make_relations_ng("expr", self.result.negative_preconditions)

        self.add_effects = make_relations_ng("expr", self.result.add_effects)
        self.del_effects = make_relations_ng("expr", self.result.del_effects)

        self.action = (self.result.name,) + self.result.parameters 
        self.action_frozenset = frozenset({self.action})
        self.action_exp = make_relations_ng("expr", self.action_frozenset)
        self.possibleactions_state[tuple(self.action_exp)] = [self.pos_precondition, self.neg_precondition, self.add_effects, self.del_effects]
 
        self.state_exp = make_relations_ng("expr", state)
        self.state_fs = FluentState(self.state_exp, [])
        self.currentstate_map = list(sorted(self.state_fs.pos, key=str))

        self.node = Node(self.state_map, self.action_exp, g, self.possibleactions_state)

    def h_pg_levelsum(self):
        """ This heuristic uses a planning graph representation of the problem
        state space to estimate the sum of the number of actions that must be
        carried out from the current state in order to satisfy each individual
        goal condition.
        --------
        Russell-Norvig 10.3.1 (3rd Edition)
        """
        pg = PlanningGraph(self.state_map, self.node.state, self.goal_pos, self.goal_neg, self.possibleactions_state)
        score = pg.h_levelsum()
        return score


    def h_pg_maxlevel(self):
            """ This heuristic uses a planning graph representation of the problem
            to estimate the maximum level cost out of all the individual goal literals.
            The level cost is the first level where a goal literal appears in the
            planning graph.
            --------
            Russell-Norvig 10.3.1 (3rd Edition)
            """
            pg = PlanningGraph(self.state_map, self.node.state, self.goal_pos, self.goal_neg, self.possibleactions_state)
            score = pg.h_maxlevel()
            return score  
          
    def h_pg_setlevel(self):
        """ This heuristic uses a planning graph representation of the problem
        to estimate the level cost in the planning graph to achieve all of the
        goal literals such that none of them are mutually exclusive.
        --------
        Russell-Norvig 10.3.1 (3rd Edition)
        """
        pg = PlanningGraph(self.state_map, self.node.state, self.goal_pos, self.goal_neg, self.possibleactions_state)
        score = pg.h_setlevel()
        return score

