from llvm import *
from llvm.core import *
from llvm.passes import *
from z3 import *

def nrecurstool(v, nbba): #Travel everywhere true to find empty keyspace
	if nbba[v][1][0] == '1':
		return (nbba[v][0] == {})
	elif nbba[v][1][0] == '2':
		return nrecurstool(int(nbba[v][1].split(', ')[-2]), nbba)
	else:
		return 0

def recurstool(v, nbba): #Travel everywhere false to find assertfail
	if nbba[v][1][0] == '4':
		return [1, v]
	elif nbba[v][1][0] == '2':
		return recurstool(int(nbba[v][1].split(', ')[-1]), nbba)
	else:
		return [0, 0] 

def recurstool1(v, nbba): #Travel everywhere true to find continuation
	if nbba[v][0] == {}:
		return v
	elif nbba[v][1][0] == '2':
		return recurstool1(int(nbba[v][1].split(', ')[-2]), nbba)
	else:
		return 0

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
		recuv = recurstool(int(ns[-1]), nbba)
		recuv1 = (recuv[0] == 1) * nrecurstool(int(ns[-2]), nbba)
		if recuv1 == 1:
			rs1 = recurs(sa + nsv, recurstool1(int(ns[-2]), nbba), reca+[ia], nbba, arga, refd)
			rs2 = recurs(sa + nsv, recuv[1], reca+[ia], nbba, arga, refd)
		else:
			sa1 = sa + nsv + vw + ns[1] + ');'
			sa2 = sa + nsv + nw + ns[1] + ');'
			rs1 = recurs(sa1, int(ns[-2]), reca+[ia], nbba, arga, refd)
			rs2 = recurs(sa2, int(ns[-1]), reca+[ia], nbba, arga, refd)
		return rs1[0] + '\n' + rs2[0] + '\n', rs1[1] + rs2[1]
	elif nbba[ia][1][0] == '3':
		return sa + 'rv:=' + ns[-1], reca + [ia]
	else: #Op signal is '4', thus an assert
		return sa + 'Assert(' + ns[-1] + ');', reca + [ia]
		
def ep(sarray, stac, sy): #Polish Notation retriever
	for si in xrange(len(sarray) - 1, -1, -1):
		if sarray[si] in sy:
			stac.append('(' + stac.pop() + ' ' + sarray[si] + ' ' + stac.pop() + ')')
		elif sarray[si] == '.':
			stac.append('Select(' + stac.pop() + ', ' + stac.pop() + ')')
		else:
			stac.append(sarray[si])
	return stac.pop()
	
def recursassert(sre):
	recui = 0
	lsre = len(sre)
	stacr = []
	values = ''
	while (recui < lsre):
		if sre[recui] == '&':
			stacr = stacr[:-1] + ['And('] + [stacr[-1]]
			values = ''
			recui = recui + 2
		elif sre[recui] == '|':
			stacr = stacr[:-1] + ['Or('] + [stacr[-1]]
			values = ''
			recui = recui + 2
		elif sre[recui] == '~':
			stacr.append('Not(')
			recui = recui + 1
		elif sre[recui] == ')':
			if values != '':
				stacr.append(values)
				if len(stacr) > 1:
					if stacr[-2] == 'Not(':
						v2 = stacr.pop()
						v1 = stacr.pop()
						stacr.append(v1 + v2 + ')')
				values = ''
			else:
				v2 = stacr.pop()
				v1 = stacr.pop()
				v0 = stacr.pop()
				stacr.append(v0 + v1 + ', ' + v2 + ')')
			recui = recui + 1
		elif sre[recui] == '(':
			values = ''
			recui = recui + 1
		else:
			values = values + sre[recui]
			recui = recui + 1
	if values != '':
		stacr.append(values)
	if stacr[0] in ['Or(', 'And(']:
		v2 = stacr.pop()
		v1 = stacr.pop()
		v0 = stacr.pop()
		stacr.append(v0 + v1 + ', ' + v2 + ')')
	return stacr[0]

def z3solve(string, array, typ):
	for vari in xrange(len(array)): #Declare all the variables
		if typ[vari] == 'Int':
			exec(array[vari] + ' = ' + 'Int(\'' + array[vari] + '\')')
		elif typ[vari] == 'Bool':
			exec(array[vari] + ' = ' + 'Bool(\'' + array[vari] + '\')')
		else:
			exec('Q = IntSort()')
			exec(array[vari] + ' = ' + 'Array(\'' + array[vari] + '\', Q, Q)')
	vte, s = eval(string), Solver()
	s.add(Not(vte))
	if s.check() == unsat:
		print 'Basic path is valid.'
	else:
		if not s.model():
			print 'Basic path is valid.'
		else:
			print 'Basic path is NOT valid. Here is a model.'
			print s.model()
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

for func in [fstruct[0]]: 
	argarray, bblocks, nar = [m.name for m in func.args], func.basic_blocks, len(func.args)
	bbln = [k.name for k in bblocks] #Name of the basic blocks
	nbbl = [[0, 0] for ni in xrange(len(bblocks))] #New blocks: [vardict, terminator]
	instrub = [[] for ini in xrange(len(bblocks))] #Instructions for each block
	cnbbl, cnbblr, assev = 0, 0, 0
	asserv, spv = 0, ''   #Assert variable
	for k in bblocks: #Get rid of unreachable blocks
		if (assev == 1):
			del nbbl[cnbbl]
			del bbln[cnbbl]
			del instrub[cnbbl]
			assev = 0
		else:
			for g in k.instructions:
				if (1 - g.is_terminator) * (1 + g.is_binary_op) == 0:
					if g.opcode_name != 'ret' and g.opcode_name != 'br':
						assev = 1
						for gk in bblocks[cnbblr + 1].instructions:
							instrub[cnbbl].append(gk)
					else:
						instrub[cnbbl].append(g)
				else:
					instrub[cnbbl].append(g)
			cnbbl = cnbbl + 1
		cnbblr = cnbblr + 1
	entryblock = func.entry_basic_block #Grab entry basic block
	for kv in xrange(len(bbln)): #Basic block #kv
		varname, varvalue = argarray[:], argarray[:]
		vardict = dict([(denum[1], denum[0]) for denum in enumerate(argarray)])
		if bbln[kv] != entryblock.name: #if basic block #kv is NOT an entry block
			varname, varvalue, vardict = [], [], dict([])
		for g in instrub[kv]: #Instructions of basic block #kv
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
						if asserv == 1: #If an assert follows:
							nbbl[kv][1] = '4, ' + spv
							asserv = 0
							spv = ''
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
					pcal = [p.name for p in g.operands]
					if pcal[-1] == '__assert_fail':  #Assert call
						pv = str(([p1 for p1 in g.operands][0].operands)[0])
						spv = pv[pv.find('\"') + 1: pv.find('\"') + pv[pv.find('\"') + 1:].find('\"') + 1]
						spv = spv[:-3]
						asserv = 1
					else: #Otherwise, call function (recursion)
						varvalue[vardict[g.name]] = 'call(' + ', '.join(pcal[:-1]) + ')'
			else: #Binary
				f, fv, fvi = ['add', 'mul', 'srem', 'sub', 'sdiv'], ['+', '*', '%', '-', '/'], 0
				for fvv in f:
					if gopname in fvv:
						break
					fvi = fvi + 1
				varvalue[vardict[g.name]] = fv[fvi] + ', ' + sop1[0] + ', ' + sop1[1]
	sym = ['+','*','%','-','/','=','!=','>','>=','<','<=','>','>=','<','<=']
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
				if d[tk][0] in ['+', '*', '%', '-', '/', '.']:
					t1, dtk = t[1].split(', '), d[tk].split(', ')
					t1v = 1 + (t1[0] == '2')
					t[1] = ', '.join(t1[:t1v] + [tk + ':=' + ep(dtk, [], sym)] + t1[t1v:])
	print nbbl
	tup = recurs('', 0, [], nbbl, argarray, [])
	tup0, tup1, tupv = [p for p in tup[0].split('\n') if p], [], [0]
	for k in tup[1][1:]:
		if k != 0:
			tupv.append(k)
		else:
			tup1, tupv = tup1 + [tupv], [0]
	tup1, basicpaths = tup1 + [tupv], []
	for ti in xrange(len(tup0)): #ti is a basic path index
		t, t1 = tup0[ti], tup1[ti][::-1] #t is basic path, t1 is reversed basic block string
		for tj in t1:
			tjkk, ntjk = [tpo for tpo in nbbl[tj][0].keys() if tpo not in argarray], nbbl[tj][0]
			loop = True
			while loop:
				loop = False
				for tjk in sorted(tjkk, key=lambda x: -len(x)):
					tv = 0
					while tv < len(t):
						if t[tv:tv+len(tjk)] == tjk:
							if (tv + len(tjk)) == len(t):
								t, tv = t[:tv] + ntjk[tjk] + t[tv + len(tjk):], tv + len(ntjk[tjk]) - 1
								loop = True
							elif (tv + len(tjk)) < len(t) and not t[tv + len(tjk)].isdigit():
								t, tv = t[:tv] + ntjk[tjk] + t[tv + len(tjk):], tv + len(ntjk[tjk]) - 1
								loop = True
						tv = tv + 1
		basicpaths.append(t)
	print '\n=======Basic Paths======='
	for bpathi in basicpaths:
		print bpathi
	fstr = raw_input('\nType the supply file you want to use: ')
	fsupply = open(fstr, 'r')
	flist = [vf.strip() for vf in list(fsupply)]
	fsupply.close()
	vararr, vartype = argarray[:], ['Int'] * len(argarray)
	for path in basicpaths:
		patha, path1, spath = path.split(';'), [], ''
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
			path1.append(v + s + (')' * (pathk[:11] == 'Assume Not(')))
		ph2, path1 = flist[-(1 + (patha[-1][:4] != 'rv:='))][:], [pk for pk in path1 if pk]
		sppp = 'Implies('
		path1asv = sum(['Assert' in sppi for sppi in path1])
		if path1asv == 1:
			sppp = 'And('
			for sppi in xrange(len(path1)):
				if path1[sppi][:7] == 'Implies':
					path1[sppi] = 'And' + path1[sppi][7:]
		for ji in xrange(len(path1) - 1, -1, -1):
			if 'Assert' in path1[ji]:
				ph2 = 'Not(' + recursassert(path1[ji][6:]) + ')'
			elif ':=' not in path1[ji]: #Not an assignment
				ph2 = path1[ji] + ', ' + ph2 + ')'
			else:
				if ':=call(' not in path1[ji]: #Not a call assignment
					o1, o2 = path1[ji][:path1[ji].index(':=')], path1[ji][path1[ji].index(':=')+2:]
					if o1 == 'rv':
						o2 = ['False', 'True'][int(o2)]
					ph2i = 0
					while (ph2i < len(ph2)):
						if (ph2[ph2i:ph2i + len(o1)] == o1):
							if not (ph2[ph2i - 1].isalnum() or ph2[ph2i - 1].isalnum()):
								ph2, ph2i = ph2[:ph2i]+'('+o2+')'+ph2[ph2i+len(o1):], ph2i+len(o2)+1
						ph2i = ph2i + 1
				else: #Is a call assignment (Remember to add rv to vararr as a boolean)
					phv, par = flist[-1][:], path1[ji][path1[ji].index(':=call(') + 7: -1].split(', ')
					stac = []
					for pari in par:
						if pari in sym:
							stac.append(pari)
						else:
							if (len(stac) < 2):
								stac.append(pari)
							elif (stac[-1] in sym):
								stac.append(pari)
							elif (stac[-2] in sym):
								op1 = stac.pop()
								stac.append('(' + op1 + ' ' + stac.pop() + ' ' + pari + ')')
							else:
								stac.append(pari)
					for oi in xrange(nar):
						o1, o2, ph2i = argarray[oi], stac[oi], 0
						if o1 != o2:
							while (ph2i < len(phv)):
								if (phv[ph2i:ph2i + len(o1)] == o1):
									if not (phv[ph2i - 1].isalnum() or phv[ph2i - 1].isalnum()):
										phv, ph2i = phv[:ph2i]+o2+phv[ph2i+len(o1):], ph2i+len(o2)+1
								ph2i = ph2i + 1
					ph2 = sppp + phv + ', ' + flist[-1][:] + ')'
					vararr, vartype = vararr + ['rv'], vartype + ['Bool']
		s, ph2i = sppp + flist[-2] + ', ' + ph2 + ')', 0
		while (ph2i < len(s)):
			if ((s[ph2i:ph2i+7] == 'ForAll(') or (s[ph2i:ph2i+7] == 'Exists(')):
				sv = s[ph2i+7:s.find(',', ph2i+7, len(s))]
				while not sv[0].isalnum():
					sv = sv[1:]
				if sv not in vararr:
					vararr, vartype = vararr + [sv], vartype + ['Int']
			elif (s[ph2i:ph2i+7] == 'Select('):
				vartype[vararr.index(s[ph2i+7:s.find(',', ph2i+7, len(s))])] = 'Array'
			ph2i = ph2i + 1
		print '\n=======Basic Path Evaluation using Z3======='
		print s
		z3solve(s, vararr, vartype)
