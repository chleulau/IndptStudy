from z3 import *

l = Int('l')
i = Int('i')
j = Int('j')
a = Array('a', IntSort(), IntSort())
u = Int('u')
e = Int('e')
n = Int('n')

v = eval('Implies(And(2 <= i, ForAll(j, Implies(And(2 <= j, j < i), n % j != 0))), Implies(i * i <= n, False == Exists(j, And(And(2 <= j, j * j <= n), n % j == 0))))')
s = Solver()
s.add(Not(v))
s.add(n == 4)
print s.check()
if s.check() == sat:
	print s.model()
