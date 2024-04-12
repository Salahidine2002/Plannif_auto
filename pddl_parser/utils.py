import collections
from itertools import product

class Expr(object):
    """A mathematical expression with an operator and 0 or more arguments.
    op is a str like '+' or 'sin'; args are Expressions.
    Expr('x') or Symbol('x') creates a symbol (a nullary Expr).
    Expr('-', x) creates a unary; Expr('+', x, 1) creates a binary."""
    __slots__ = ["op", "args", "__hash"]
    def __init__(self, op, *args):
        self.op = op
        self.args = args
        self.__hash = hash(self.op) ^ hash(self.args)

    def __eq__(self, other):
        return (isinstance(other, Expr)
                and self.op == other.op
                and self.args == other.args)

    def __hash__(self): return self.__hash

    # custom unary operator overloads to handle 
    def __pos__(self): return self
    def __neg__(self): return self.args[0] if '-' == self.op else Expr("-", self)
    def __invert__(self): return self.args[0] if '~' == self.op else Expr("~", self)

    # Operator overloads
    # def __neg__(self): return Expr('-', self)
    # def __pos__(self): return Expr('+', self)
    # def __invert__(self): return Expr('~', self)
    def __add__(self, rhs): return Expr('+', self, rhs)
    def __sub__(self, rhs): return Expr('-', self, rhs)
    def __mul__(self, rhs): return Expr('*', self, rhs)
    def __pow__(self, rhs): return Expr('**', self, rhs)
    def __mod__(self, rhs): return Expr('%', self, rhs)
    def __and__(self, rhs): return Expr('&', self, rhs)
    def __xor__(self, rhs): return Expr('^', self, rhs)
    def __rshift__(self, rhs): return Expr('>>', self, rhs)
    def __lshift__(self, rhs): return Expr('<<', self, rhs)
    def __truediv__(self, rhs): return Expr('/', self, rhs)
    def __floordiv__(self, rhs): return Expr('//', self, rhs)
    def __matmul__(self, rhs): return Expr('@', self, rhs)

    def __or__(self, rhs):
        """Allow both P | Q, and P |'==>'| Q."""
        if isinstance(rhs, Expression):
            return Expr('|', self, rhs)
        else:
            return PartialExpr(rhs, self)

    # Reverse operator overloads
    def __radd__(self, lhs): return Expr('+', lhs, self)
    def __rsub__(self, lhs): return Expr('-', lhs, self)
    def __rmul__(self, lhs): return Expr('*', lhs, self)
    def __rdiv__(self, lhs): return Expr('/', lhs, self)
    def __rpow__(self, lhs): return Expr('**', lhs, self)
    def __rmod__(self, lhs): return Expr('%', lhs, self)
    def __rand__(self, lhs): return Expr('&', lhs, self)
    def __rxor__(self, lhs): return Expr('^', lhs, self)
    def __ror__(self, lhs): return Expr('|', lhs, self)
    def __rrshift__(self, lhs): return Expr('>>', lhs, self)
    def __rlshift__(self, lhs): return Expr('<<', lhs, self)
    def __rtruediv__(self, lhs): return Expr('/', lhs, self)
    def __rfloordiv__(self, lhs): return Expr('//', lhs, self)
    def __rmatmul__(self, lhs): return Expr('@', lhs, self)

    def __call__(self, *args):
        "Call: if 'f' is a Symbol, then f(0) == Expr('f', 0)."
        if self.args:
            raise ValueError('can only do a call for a Symbol, not an Expr')
        else:
            return Expr(self.op, *args)

    def __repr__(self):
        op = self.op
        args = [str(arg) for arg in self.args]
        if op.isidentifier():       # f(x) or f(x, y)
            return '{}({})'.format(op, ', '.join(args)) if args else op
        elif len(args) == 1:        # -x or -(x + 1)
            return op + args[0]
        else:                       # (x - y)
            opp = (' ' + op + ' ')
            return '(' + opp.join(args) + ')'

# An 'Expression' is either an Expr or a Number.
# Symbol is not an explicit type; it is any Expr with 0 args.

Number = (int, float, complex)
Expression = (Expr, Number)


def Symbol(name):
    "A Symbol is just an Expr with no args."
    return Expr(name)


def symbols(names):
    "Return a tuple of Symbols; names is a comma/whitespace delimited str."
    return tuple(Symbol(name) for name in names.replace(',', ' ').split())


def subexpressions(x):
    "Yield the subexpressions of an Expression (including x itself)."
    yield x
    if isinstance(x, Expr):
        for arg in x.args:
            yield from subexpressions(arg)


def arity(expression):
    "The number of sub-expressions in this expression."
    if isinstance(expression, Expr):
        return len(expression.args)
    else:  # expression is a number
        return 0
def expr_handle_infix_ops(x):
    """Given a str, return a new str with ==> replaced by |'==>'|, etc.
    >>> expr_handle_infix_ops('P ==> Q')
    "P |'==>'| Q"
    """
    for op in infix_ops:
        x = x.replace(op, '|' + repr(op) + '|')
    return x


class defaultkeydict(collections.defaultdict):
    """Like defaultdict, but the default_factory is a function of the key.
    >>> d = defaultkeydict(len); d['four']
    4
    """
    def __missing__(self, key):
        self[key] = result = self.default_factory(key)
        return result
        
def expr(x):
    """Shortcut to create an Expression. x is a str in which:
    - identifiers are automatically defined as Symbols.
    - ==> is treated as an infix |'==>'|, as are <== and <=>.
    If x is already an Expression, it is returned unchanged. Example:
    >>> expr('P & Q ==> Q')
    ((P & Q) ==> Q)
    """
    if isinstance(x, str):
        return eval(expr_handle_infix_ops(x), defaultkeydict(Symbol))
    else:
        return x

infix_ops = '==> <== <=>'.split()    
    
def associate(op, args):
    """Given an associative op, return an expression with the same
    meaning as Expr(op, *args), but flattened -- that is, with nested
    instances of the same op promoted to the top level.
    >>> associate('&', [(A&B),(B|C),(B&C)])
    (A & B & (B | C) & B & C)
    >>> associate('|', [A|(B|(C|(A&B)))])
    (A | B | C | (A & B))
    """
    args = dissociate(op, args)
    if len(args) == 0:
        return _op_identity[op]
    elif len(args) == 1:
        return args[0]
    else:
        return Expr(op, *args)

_op_identity = {'&': True, '|': False, '+': 0, '*': 1}    

def create_expressions(str_list):
    """ Converts a list of strings into a list of Expr objects """
    return [expr(s) for s in str_list]
    
def make_relations(name, *args, key=lambda x: True):
    """ Map the arguments to expressions. the first positional arg is used as the expression name
    and all remaining expressions are used as arguments.

    Expressions are made over the cartesian product of the positional arguments after the name.
    The expressions can be filtered by supplying a function `key` that takes a length k tuple
    and returns a boolean False for the elements that should be excluded, where k is the number
    of positional arguments after "name".

    Example
    -------
    
    >>> make_relations("At", ["Cargo1", "PlaneA"], ["Airport1"])

        [expr(At(Cargo1, Airport1)), expr(At(PlaneA, Airport1))]

    To filter out the expressions for Airport1, use:

    >>> make_relations("At", ["Cargo1", "PlaneA"], ["Airport1", "Airport2"], key=lambda x: x[-1].endswith("2"))

        [expr(At(Cargo1, Airport2)), expr(At(PlaneA, Airport2))]

    See additional examples in example_have_cake.py and air_cargo_problems.py 
    """


    return create_expressions("{}({})".format(name, ", ".join(c)) for c in product(*args) if key(c))

def make_relations_ng(name, state):
    """Create expressions from the state tuples."""
    expr_list = []
    for item in state:
        args = [repr(arg) for arg in item]  # Convert each element of the tuple to a string representation
        expr_str = "{}({})".format(name, ", ".join(args))
        expr_list.append(expr(expr_str))
    return expr_list

class FluentState:
    """ Represent planning problem states as positive and negative fluents """
    def __init__(self, pos_list, neg_list):
        self.pos = list(pos_list)
        self.neg = list(neg_list)

    def sentence(self):
        return expr(conjunctive_sentence(self.pos, self.neg))

    def pos_sentence(self):
        return expr(conjunctive_sentence(self.pos, []))


def conjunctive_sentence(pos_list, neg_list):
    """ Express a state as a conjunctive sentence from positive and negative fluent lists

    Parameters
    ----------
    pos_list:
        an iterable collection of strings or Expr representing fluent literals that
        are True in the current state

    neg_list:
        an iterable collection of strings or Expr representing fluent literals that
        are False in the current state

    Returns
    -------
    A conjunctive sentence (i.e., a sequence of clauses connected by logical AND)
    e.g. "At(C1, SFO) ∧ ~At(P1, SFO)"
    """
    clauses = []
    for f in pos_list:
        clauses.append(expr("{}".format(f)))
    for f in neg_list:
        clauses.append(expr("~{}".format(f)))
    return associate('&', clauses)
    

def encode_state(fs, fluent_map):
    """ Convert a FluentState (list of positive fluents and negative fluents) into
    an ordered sequence of True/False values.

    It is sometimes convenient to encode a problem in terms of the specific
    fluents that are True or False in a state, but other times it is easier (or faster)
    to perform computations on an an array of booleans.

    Parameters
    ----------
    fs: FluentState
        A state object represented as a FluentState

    fluent_map:
        An ordered sequence of fluents
    
    Returns
    -------
    tuple of True/False elements corresponding to the fluents in fluent_map
    """
    return tuple([f in fs.pos for f in fluent_map])


def decode_state(state, fluent_map):
    """ Convert an ordered list of True/False values into a FluentState
    (list of positive fluents and negative fluents)

    It is sometimes convenient to encode a problem in terms of the specific
    fluents that are True or False in a state, but other times it is easier (or faster)
    to perform computations on an an array of booleans.

    Parameters
    ----------
    state:
        A state represented as an ordered sequence of True/False values

    fluent_map:
        An ordered sequence of fluents

    Returns
    -------
    FluentState instance containing the fluents from fluent_map corresponding to True
    entries from the input state in the pos_list, and containing the fluents from
    fluent_map corresponding to False entries in the neg_list
    """
    fs = FluentState(set(), set())
    for idx, elem in enumerate(state):
        if elem:
            fs.pos.append(fluent_map[idx])
        else:
            fs.neg.append(fluent_map[idx])
    return fs   



class Action:
    """
    Defines an action schema using preconditions and effects
    Use this to describe actions in PDDL
    action is an Expr where variables are given as arguments(args)
    Precondition and effect are both lists with positive and negated literals
    Example:
    precond_pos = [expr("Human(person)"), expr("Hungry(Person)")]
    precond_neg = [expr("Eaten(food)")]
    effect_add = [expr("Eaten(food)")]
    effect_rem = [expr("Hungry(person)")]
    eat = Action(expr("Eat(person, food)"), [precond_pos, precond_neg], [effect_add, effect_rem])
    """

    def __init__(self, action, precond, effect):
        self.name = action.op
        self.args = action.args
        self.precond_pos = set(precond[0])
        self.precond_neg = set(precond[1])
        self.effect_add = set(effect[0])
        self.effect_rem = set(effect[1])

    def __call__(self, kb, args):
        return self.act(kb, args)

    def __str__(self):
        return "{}{!s}".format(self.name, self.args)

    def substitute(self, e, args):
        """Replaces variables in expression with their respective Propostional symbol"""
        new_args = list(e.args)
        for num, x in enumerate(e.args):
            for i in range(len(self.args)):
                if self.args[i] == x:
                    new_args[num] = args[i]
        return Expr(e.op, *new_args)

    def check_precond(self, kb, args):
        """Checks if the precondition is satisfied in the current state"""
        # check for positive clauses
        for clause in self.precond_pos:
            if self.substitute(clause, args) not in kb.clauses:
                return False
        # check for negative clauses
        for clause in self.precond_neg:
            if self.substitute(clause, args) in kb.clauses:
                return False
        return True

    def act(self, kb, args):
        """Executes the action on the state's kb"""
        # check if the preconditions are satisfied
        if not self.check_precond(kb, args):
            raise Exception("Action pre-conditions not satisfied")
        # remove negative literals
        for clause in self.effect_rem:
            kb.retract(self.substitute(clause, args))
        # add positive literals
        for clause in self.effect_add:
            kb.tell(self.substitute(clause, args))