from pddl_prover import *
import pddl 

domain = pddl.parse_domain('./Group1/domain_lights_out.pddl')
problem = pddl.parse_problem('./Group1/problems/lights_size3x3_conf1.pddl')

l0, l1, l2, l3  =  Constant(0), Constant(1), Constant(2), Constant(3)
l  =  Variable('l')

on  =  Predicate('on', 1)
turnoff = Predicate('turnoff', 1)


# Note: atoms in the knowledge base can be represented either in tuple form or as instances of the class logic.Atom
kb  = ({l0,l1,l2, l3},{('on',(0,)), not ('on',(1,)), ('on',(2,)), not ('on',(3,))})



print("Evaluation:", (on(l0)).evaluate(kb)) # True
print("Evaluation:", (on(l1)).evaluate(kb)) # True
print("Evaluation:", (on(l2)).evaluate(kb)) # True
print("Evaluation:", (on(l3)).evaluate(kb)) # True

count = Count(on(l), l).evaluate(kb)
print("Evaluation:", count[0]) # True

for answer in count[1] : 
    # print([name for name in dir(answer[l]) if not name.startswith('_')]) 
    print(answer[l].name)

# print("Evaluation:", handempty().evaluate(kb)) # True
# print("Evaluation:", (ontable(b0) & on(b1,b0)).evaluate(kb)) # True
# print("Evaluation:", TE(x, on(x,b0)).evaluate(kb)) # There Exists some x for which on(x,b0) -> True
# print("Evaluation:", (TE(x, ontable(x)) == 1).evaluate(kb)) # There exists <only> one object for which ontable(x) is True -> True (counting quantifier)
# print("Number of true substitutions:", Count(on(x,y), x, y).evaluate(kb)[0]) # Returns the numbe

print(domain.actions)

print([name for name in dir(problem) if not name.startswith('_')])

# print(problem.goal)
print(list(problem.init)[1])
print(problem.objects)
