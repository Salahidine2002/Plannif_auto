from .planning_graph import PlanningGraph, Node  # Assuming you have a PlanningGraph class defined elsewhere
from .utils import encode_state, decode_state, make_relations_ng, FluentState

class BasePlanningProblem:
    def __init__(self, initial, state, goal_pos, goal_neg, result, g):
        self.possibleactions_state = {}
        self.expressions = make_relations_ng("expr", initial)
        self.pos = self.expressions
        self.neg = []
        self.initial = FluentState(self.pos, self.neg)
        #print("goal_pos", goal_pos)
        self.goal_pos = make_relations_ng("expr", goal_pos)
        self.goal_neg = make_relations_ng("expr", goal_neg)
        self.goals = FluentState(self.goal_pos, self.goal_neg)
        self.state_map = list(sorted(self.initial.pos+self.initial.neg, key=str))
        #print("State map: ", self.state_map)
        self.result = result
        self.pos_precondition = make_relations_ng("expr", self.result.positive_preconditions)
        self.neg_precondition = make_relations_ng("expr", self.result.negative_preconditions)
        self.add_effects = make_relations_ng("expr", self.result.add_effects)
        self.del_effects = make_relations_ng("expr", self.result.del_effects)
        #self.parameters = make_relations_ng("expr", self.result.parameters)
        self.action = (self.result.name,) + self.result.parameters 
        #print("Action: ", self.action)
        self.action_frozenset = frozenset({self.action})
        self.action_exp = make_relations_ng("expr", self.action_frozenset)
        #print("Action exp: ", self.action_exp)
        self.possibleactions_state[tuple(self.action_exp)] = [self.pos_precondition, self.neg_precondition, self.add_effects, self.del_effects]
        #print("All possible actions in this state: ", self.possibleactions_state)

        # print(actions)
        # self.actions = make_relations_ng("expr", actions)
        # self.app_actions = list(sorted(self.actions, key=str))


        self.state_exp = make_relations_ng("expr", state)
        self.state_fs = FluentState(self.state_exp, [])
        self.currentstate_map = list(sorted(self.state_fs.pos, key=str))


        #print("Positive Precond.: ", self.pos_precondition)
        #self.initial_state_TF = encode_state(initial, self.state_map)
        self.node = Node(self.state_map, self.action_exp, g, self.possibleactions_state)
        #print("Node: ", self.node)
        #print("Node state: ", self.node.state)
        
        
        #super().__init__(self.initial_state_TF, goal=goal)

    def h_pg_levelsum(self):
        """ This heuristic uses a planning graph representation of the problem
        state space to estimate the sum of the number of actions that must be
        carried out from the current state in order to satisfy each individual
        goal condition.

        See Also
        --------
        Russell-Norvig 10.3.1 (3rd Edition)
        """
        pg = PlanningGraph(self.state_map, self.node.state, self.goal_pos, self.goal_neg, self.possibleactions_state)
        score = pg.h_levelsum()
        return score
    