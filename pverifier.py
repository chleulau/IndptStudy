from llvm import *
from llvm.core import *
from llvm.passes import *
from z3 import *

def recurs(sa, ia, reca, nbba, arga, refd):
	if ia in reca:
		return sa, reca
	ns, vw, nw, v = nbba[ia][1].split(', '), 'Assume (', 'Assume Not(', ''
	if nbba[ia][1][0] == '1':
		nsv = ''
		for nsvi in xrange(1, len(ns) - 1):
			nsv = nsv + ns[nsvi] + ';'
		v = recurs(sa + nsv, int(ns[-1]), reca + [ia], nbba, arga, refd)
		return v[0], v[1]
	elif nbba[ia][1][0] == '2':
		nsv = ''
		for nsvi in xrange(2, len(ns) - 2):
			nsv = nsv + ns[nsvi] + ';'
		rs1 = recurs(sa + nsv + vw + ns[1] + ');', int(ns[-2]), reca+[ia], nbba, arga, refd)
		rs2 = recurs(sa + nsv + nw + ns[1] + ');', int(ns[-1]), reca+[ia], nbba, arga, refd)
		return rs1[0] + '\n' + rs2[0] + '\n', rs1[1] + rs2[1]
	else:
		return sa + 'rv:=' + ns[-1], reca + [ia]
		
def ep(sarray, stac, sy): #Polish Notation retriever
	for si in xrange(len(sarray) - 1, -1, -1):
		if sarray[si] in sy:
			stac.append('(' + stac.pop() + ' ' + sarray[si] + ' ' + stac.pop() + ')')
		elif sarray[si] == '.':
			stac.append('Select(' + stac.pop() + ', ' + stac.pop() + ')')
		else:
			stac.append(sarray[si])
	return stac.pop()

def z3solve(string, array, typ):
	for vari in xrange(len(array)): #Declare all the variables
		if typ[vari] == 'Int':
			exec(array[vari] + ' = ' + 'Int(\'' + array[vari] + '\')')
		else:
			exec('Q = IntSort()')
			exec(array[vari] + ' = ' + 'Array(\'' + array[vari] + '\', Q, Q)')
	vte, s = eval(string), Solver()
	s.add(Not(vte))
	if s.check() == unsat:
		print 'Basic path is valid.'
	return None

fstr = raw_input('Type the LLVM file you want to verify: ')
llfile = file(fstr)
mymod = Module.from_assembly(llfile) #Module of the llvm file

#Use -instnamer LLVM pass to rename instructions for easier usage
pm = PassManager.new()
pm.add(PASS_INSTNAMER)
pm.run(mymod)

fstruct = [] #Function structures from module (there's only one: func)
for f in mymod.functions:
	fstruct.append(mymod.get_function_named(f.name))

for func in fstruct: 
	argarray, bblocks = [m.name for m in func.args], func.basic_blocks
	bbln = [k.name for k in bblocks] #Name of the basic blocks
	nbbl = [[0, 0] for ni in xrange(len(bblocks))] #New blocks: [vardict, terminator]
	entryblock = func.entry_basic_block #Grab entry basic block
	for k in bblocks: #Basic block k
		varname, varvalue = argarray[:], argarray[:]
		vardict = dict([(denum[1], denum[0]) for denum in enumerate(argarray)])
		kv = bbln.index(k.name)
		if k.name != entryblock.name: #if k is NOT an entry block
			varname, varvalue, vardict = [], [], dict([])
		for g in k.instructions: #Instructions of basic block k
			v = (1 - g.is_terminator) * (1 + g.is_binary_op) #0: Term, 1: Non-bin, 2: Bin
			gopr, sop1, gopname = g.operands, [], g.opcode_name #Analysis items for g
			for operv in gopr:
				if str(operv.name) == '': #If the first element is a ConstantInt
					sop1.append(str(operv)[str(operv).rfind(' ') + 1:])
				else:
					sop1.append(str(operv.name))
			if (g.name) and (g.name not in varname):
				varname.append(g.name)
				varvalue.append('0')
				vardict[g.name] = len(varname) - 1
			if (g.name) and (g.name[:3] != 'tmp'):
				argarray.append(g.name)
			if v == 0: #Terminating
				nd = dict([(varname[ndi], varvalue[ndi]) for ndi in xrange(len(varname))])
				nbbl[kv][0] = nd.copy()
				if gopname == 'ret':
					nbbl[kv][1] = '3, ' + sop1[0]
				elif gopname == 'br':
					if len(sop1) == 1:
						nbbl[kv][1] = '1, ' + str(bbln.index(sop1[0]))
					else:
						#g.operands reverses last two operands?
						nbbl[kv][1] = '2, ' + sop1[0] + ', ' + str(bbln.index(sop1[2]))
						nbbl[kv][1] = nbbl[kv][1] + ', ' + str(bbln.index(sop1[1]))
			elif v == 1: #Non-binary
				if gopname == 'alloca':
					varvalue[vardict[g.name]] = '0'
				elif gopname == 'load' or gopname == 'sext':
					varvalue[vardict[g.name]] = sop1[0]
				elif gopname == 'store':
					if sop1[1] not in varname:
						varname.append(sop1[1])
						varvalue.append('0')
						vardict[sop1[1]] = len(varname) - 1
					varvalue[vardict[sop1[1]]] = sop1[0]
				elif gopname == 'getelementptr':
					varvalue[vardict[g.name]] = '.' + ', ' + sop1[0] + ', ' + sop1[1]
				elif gopname == 'icmp':
					fv = ['=','!=','>','>=','<','<=','>','>=','<','<='][int(g.predicate) - 32]
					varvalue[vardict[g.name]] = fv + ', ' + sop1[0] + ', ' + sop1[1]
				elif gopname == 'call':
					varvalue[vardict[g.name]] = 'call function'
			else: #Binary
				f, fv, fvi = ['add', 'mul', 'srem', 'sub'], ['+', '*', '%', '-'], 0
				for fvv in f:
					if gopname in fvv:
						break
					fvi = fvi + 1
				varvalue[vardict[g.name]] = fv[fvi] + ', ' + sop1[0] + ', ' + sop1[1]
	sym = ['+','*','%','-','=','!=','>','>=','<','<=','>','>=','<','<=']
	for t in nbbl:
		d, bkeys, loop = t[0], t[0].keys(), True
		while loop:
			loop = False
			for bk in [vo for vo in bkeys]:
				vbk, vbknew = d[bk].split(', '), []
				for vbkv in vbk:
					newv = vbkv
					if newv in bkeys and (newv not in argarray) and newv != d[newv]:
						newv, loop = d[newv], True
						while ((newv in d.keys()) and (newv not in argarray) and (newv != d[newv])):
							newv = d[newv]
					vbknew.append(newv)
				d[bk] = ', '.join(vbknew)
		for tk in bkeys:
			if tk in argarray:
				if d[tk][0] in ['+', '*', '%', '-', '.']:
					t1, dtk = t[1].split(', '), d[tk].split(', ')
					t1v = 1 + (t1[0] == '2')
					t[1] = ', '.join(t1[:t1v] + [tk + ':=' + ep(dtk, [], sym)] + t1[t1v:])
	tup = recurs('', 0, [], nbbl, argarray, [])
	tup0, tup1, tupv = [p for p in tup[0].split('\n') if p], [], [0]
	for k in tup[1][1:]:
		if k != 0:
			tupv.append(k)
		else:
			tup1, tupv = tup1 + [tupv], [0]
	tup1, basicpaths = tup1 + [tupv], []
	for ti in xrange(len(tup0)):
		t, t1 = tup0[ti], tup1[ti][::-1]
		for tj in t1:
			tjkk, ntjk = [tpo for tpo in nbbl[tj][0].keys() if tpo not in argarray], nbbl[tj][0]
			for tjk in sorted(tjkk, key=lambda x: -len(x)):
				tv = 0
				while tv < len(t):
					if t[tv:tv+len(tjk)] == tjk:
						if (tv + len(tjk)) == len(t):
							t, tv = t[:tv] + ntjk[tjk] + t[tv + len(tjk):], tv + len(ntjk[tjk]) - 1
						elif (tv + len(tjk)) < len(t) and not t[tv + len(tjk)].isdigit():
							t, tv = t[:tv] + ntjk[tjk] + t[tv + len(tjk):], tv + len(ntjk[tjk]) - 1
					tv = tv + 1
		basicpaths.append(t)
	print '=======Basic Paths======='
	for bpathi in basicpaths:
		print bpathi
	bpaths = []
	for path in basicpaths:
		patha, pathall, spath = path.split(';'), [], ''
		for pathk in patha:
			s, v = pathk, ''
			if pathk[:8] == 'Assume (':
				s, v = pathk[8:-1], 'Implies('
			elif pathk[:11] == 'Assume Not(':
				s, v = pathk[11:-1], 'Implies(Not('
			if v:
				s, ph2i = ep(s.split(', '), [], sym), 0
				while (ph2i < len(s)): #Find '=' and replace with '=='
					if (s[ph2i:ph2i + 3] == ' = '):
						s, ph2i = s[:ph2i]+' == '+s[ph2i+3:], ph2i+3
					ph2i = ph2i + 1
			pathall.append(v + s + (')' * (pathk[:11] == 'Assume Not(')))
		spath, paren, trm = pathall[0], pathall[0][:8] == 'Implies(', patha[-1][:4] == 'rv:='
		for pathi in pathall[1:]:
				spath = spath + ', ' + (';' * (pathi[:8] != 'Implies(')) + pathi 
				paren = paren + (pathi[:8] == 'Implies(')
		bpaths.append([spath, int(paren), trm])
	fstr = raw_input('Type the supply file you want to use: ')
	fsupply = open(fstr, 'r')
	flist = [vf.strip() for vf in list(fsupply)]
	fsupply.close()
	for path in bpaths:
		path1, ph2 = path[0].split(';'), flist[1 + path[2]][:]
		for ji in xrange(len(path1) - 1, -1, -1):
			if ':=' not in path1[ji]:
				break
			else:
				o1, o2 = path1[ji][:path1[ji].index(':=')], path1[ji][path1[ji].index(':=')+2:]
				if o1 == 'rv':
					o2 = ['False', 'True'][int(o2)]
				ph2i = 0
				while (ph2i < len(ph2)):
					if (ph2[ph2i:ph2i + len(o1)] == o1):
						if not (ph2[ph2i - 1].isalnum() or ph2[ph2i - 1].isalnum()):
							ph2, ph2i = ph2[:ph2i]+'('+o2+')'+ph2[ph2i+len(o1):], ph2i+len(o2)+1
					ph2i = ph2i + 1
		s = 'Implies(' + flist[1] + ', ' + path1[0] + ph2 + (')' * (path[1] + 1))
		vararr, vartype, ph2i = argarray[:], ['Int'] * len(argarray), 0
		while (ph2i < len(s)):
			if ((s[ph2i:ph2i+7] == 'ForAll(') or (s[ph2i:ph2i+7] == 'Exists(')):
				sv = s[ph2i+7:s.find(',', ph2i+7, len(s))]
				if sv not in vararr:
					vararr, vartype = vararr + [sv], vartype + ['Int']
			elif (s[ph2i:ph2i+7] == 'Select('):
				vartype[vararr.index(s[ph2i+7:s.find(',', ph2i+7, len(s))])] = 'Array'
			ph2i = ph2i + 1
		print '=======Basic Path Evaluation using Z3======='
		print s
		z3solve(s, vararr, vartype)
