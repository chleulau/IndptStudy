#General-purpose parser

#Unconditional loop parser (mainly for for loops)
def uncloop(lines, label, looplabels, text, labelnames, labelplaces, varnames, varvalues):
	
	#If we already have seen the label before, exit
	if label in looplabels:
		if text[-5:] == ' and ':
			text = text[:-5]
		return text
	
	looplabels1 = looplabels[:]
	looplabels1.append(label)
	labelindex = labelnames.index(label)
	loop_index = labelplaces[labelindex]
	tempvar_names = []
	tempvar_values = []
	lline = lines[loop_index]
	lline = lline.strip('\n')
	lline = lline.strip()
	while lline:
	
		temptext = ''
	
		#If loading a temporary variable
		if ' load ' in lline:
			v_name = lline[0:lline[0:].find(' ')]
			valueline = lline[lline.find('load'):]
			if valueline.find(',') == -1:
				value_name = valueline[valueline.find('%'):]
			else:
				value_name = valueline[valueline.find('%'): valueline.find(',')]
			while (value_name in tempvar_names):
				value_name = tempvar_values[tempvar_names.index(value_name)]
			if value_name in varnames:
				value_n = str(varvalues[varnames.index(value_name)])
				if (value_n in varnames):
					value_name = value_n
			if v_name not in tempvar_names:
				tempvar_names.append(v_name)
				tempvar_values.append(value_name)
			else:
				tempvar_values[tempvar_names.index(v_name)] = value_name
		
		#If turning a variable into another
		if ' sext ' in lline:
			v_name = lline[0:lline[0:].find(' ')]
			valueline = lline[lline.find('sext'):]
			valueline = valueline[valueline.find('%'):]
			value_name = valueline[valueline.find('%'): valueline.find(' ')]
			while (value_name in tempvar_names):
				value_name = tempvar_values[tempvar_names.index(value_name)]
			if value_name in varnames:
				value_n = str(varvalues[varnames.index(value_name)])
				if (value_n in varnames):
					value_name = value_n
			if v_name not in tempvar_names:
				tempvar_names.append(v_name)
				tempvar_values.append(value_name)
			else:
				tempvar_values[tempvar_names.index(v_name)] = value_name
		
		#If comparing two variables
		elif ' icmp ' in lline:
			flags = ['eq', 'ne', 'ugt', 'uge', 'ult', 'ule', 'sgt', 'sge', 'slt', 'sle']
			flag_value = ['=', '!=', '>', '>=', '<', '<=', '>', '>=', '<', '<=']
			v_name = lline[0:lline[0:].find(' ')]
			tempvar_names.append(v_name)
			valueline = lline[lline.find('icmp'):]
			value_op = valueline[valueline.find(' ') + 1: valueline.find(' i')]
			value_op = flag_value[flags.index(value_op)]
			value_name = valueline[valueline.find('%'): valueline.find(',')]
			value_name = tempvar_values[tempvar_names.index(value_name)]
			value_compvalue = valueline[valueline.find(',') + 2:]
			if value_compvalue in tempvar_names:
				value_compvalue = tempvar_values[tempvar_names.index(value_compvalue)]
			temptext = value_name + ' ' + value_op + ' ' + value_compvalue
			
		#If adding two variables
		elif ' add ' in lline:
			valueline = lline[lline.find('add'):]
			value_name = valueline[valueline.find('%'): valueline.find(',')]
			value_name = tempvar_values[tempvar_names.index(value_name)]
			value_compvalue = valueline[valueline.find(',') + 2:]
			if value_compvalue in tempvar_names:
				value_compvalue = tempvar_values[tempvar_names.index(value_compvalue)]
			addtext = value_name + ' + ' + value_compvalue
			v_name = lline[0:lline[0:].find(' ')]
			if v_name not in tempvar_names:
				tempvar_names.append(v_name)
				tempvar_values.append(addtext)
			else:
				tempvar_values[tempvar_names.index(v_name)] = addtext
		
		#If multiplying two variables
		elif ' mul ' in lline:
			valueline = lline[lline.find('mul'):]
			value_name = valueline[valueline.find('%'): valueline.find(',')]
			value_name = tempvar_values[tempvar_names.index(value_name)]
			value_compvalue = valueline[valueline.find(',') + 2:]
			if value_compvalue in tempvar_names:
				value_compvalue = tempvar_values[tempvar_names.index(value_compvalue)]
			multext = value_name + ' * ' + value_compvalue
			v_name = lline[0:lline[0:].find(' ')]
			if v_name not in tempvar_names:
				tempvar_names.append(v_name)
				tempvar_values.append(multext)
			else:
				tempvar_values[tempvar_names.index(v_name)] = multext
		
		#If remaindering two variables
		elif ' srem ' in lline:
			valueline = lline[lline.find('srem'):]
			value_name = valueline[valueline.find('%'): valueline.find(',')]
			value_name = tempvar_values[tempvar_names.index(value_name)]
			value_compvalue = valueline[valueline.find(',') + 2:]
			if value_compvalue in tempvar_names:
				value_compvalue = tempvar_values[tempvar_names.index(value_compvalue)]
			sremtext = value_name + ' % ' + value_compvalue
			v_name = lline[0:lline[0:].find(' ')]
			if v_name not in tempvar_names:
				tempvar_names.append(v_name)
				tempvar_values.append(sremtext)
			else:
				tempvar_values[tempvar_names.index(v_name)] = sremtext
		
		#If remaindering two variables
		elif ' getelementptr ' in lline:
			valueline = lline[lline.find('getelementptr'):]
			value_name = valueline[valueline.find('%'): valueline.find(',')]
			value_name = tempvar_values[tempvar_names.index(value_name)]
			value_compline = valueline[valueline.find(','):]
			value_compvalue = value_compline[value_compline.find('%'):]
			if value_compvalue in tempvar_names:
				value_compvalue = tempvar_values[tempvar_names.index(value_compvalue)]
			ptrtext = value_name + '[' + value_compvalue + ']'
			v_name = lline[0:lline[0:].find(' ')]
			if v_name not in tempvar_names:
				tempvar_names.append(v_name)
				tempvar_values.append(ptrtext)
			else:
				tempvar_values[tempvar_names.index(v_name)] = ptrtext
		
		elif 'ret ' in lline:
			retline = lline[lline.find(' ') + 1:]
			retvalue = retline[retline.find(' ') + 1:]
			if retvalue == '0':
				text = text + 'rv = 0\n'
			else:
				if retvalue in tempvar_names:
					retvalue = tempvar_values[tempvar_names.index(retvalue)]
				if retvalue in varnames:
					retvalue = varvalues[varnames.index(retvalue)]
				text = text + 'rv = ' + retvalue
		
		#If it hits a branch
		elif lline[0:3] == 'br ':
			if lline.find(',') == -1:
				labeltext = lline[lline.find('label '):]
				labelname = labeltext[labeltext.find(' '):][1:]
				if text:
					text = text + ' and '
				text = uncloop(lines, labelname, looplabels1, text, labelnames, labelplaces, varnames, varvalues)
			else:
				labeltext = lline[lline.find('label '):]
				labelname1 = labeltext[labeltext.find(' ') + 1:labeltext.find(',')]
				labeltext2 = labeltext[labeltext.find(', label ') + 2:]
				labelname2 = labeltext2[labeltext2.find(' ') + 1:]
				text1 = uncloop(lines, labelname1, looplabels1, '', labelnames, labelplaces, varnames, varvalues)
				text2 = uncloop(lines, labelname2, looplabels1, '', labelnames, labelplaces, varnames, varvalues)
				text = 'If ' + text + ':\nthen ' + text1 + '\nOtherwise: ' + text2 + '\n'
		
		#Move to next line
		loop_index = loop_index + 1
		lline = lines[loop_index]
		lline = lline.strip('\n')
		lline = lline.strip()
		
		#If next line has the word "store" in it, change text to suit this
		if lline[0:6] == 'store ':
			
			#First find value to add, whether it is string or number
			lline1 = lline[6:]
			var_src = lline1[lline1.find(' ') + 1:lline1.find(',')]
			if var_src.replace('.','',1).isdigit():
				var_src = int(var_src)
			else:
				var_src = tempvar_values[tempvar_names.index(var_src)]
			var_src = str(var_src)
			
			#Then find variable to store to, and store value to variable
			lline1 = lline1[lline1.find(',') + 2:]
			lline1_end = lline1.find(',')
			var_dst = ''
			if lline1_end != -1:
				var_dst = lline1[lline1.find(' ') + 1:lline1_end]
			else:
				var_dst = lline1[lline1.find(' ') + 1:]
			if var_dst not in tempvar_names:
				tempvar_names.append(var_dst)
				tempvar_values.append(var_src)
			else:
				tempvar_values[tempvar_names.index(var_dst)] = var_src
			if var_dst in varnames:
				varvalues[varnames.index(var_dst)] = var_src
			
			#Print to text only the variables that aren't for temp storage.
			if var_dst in varnames and not var_dst[1:].isdigit():
				if text == '':
					text = var_dst + " = " + var_src
				else:
					if text[-5:] != ' and ':
						text = text + ' and ' + var_dst + " = " + var_src
					else:
						text = text + var_dst + " = " + var_src
			
			loop_index = loop_index + 1
			lline = lines[loop_index]
			lline = lline.strip('\n')
			lline = lline.strip()
		
		else:
			if temptext != '':
				if text == '':
					text = temptext
				else:
					text = text + ' and ' + temptext
	return text

#renamer for logic text s
def renamer(s):
	t = ''
	for i in xrange(len(s)):
		if s[i] != '%':
			t = t + s[i]
		else:
			if (s[i - 1] == ' ') and (s[i + 1] == ' '):
				t = t + s[i]
	return [i for i in t.split('\n') if i]

#recursive parser for logic text array a
def logiparser(a, position, rootposition, rootvalue, text):
	te = ''
	sentence = a[position]
	
	#if sentence starts with "if"
	if sentence[0:3] == 'If ':
		rootposition.append(position)
		rootvalue.append(len(text))
		te = logiparser(a, position + 1, rootposition, rootvalue, text + '(' + sentence[3:-1] + ')')
	
	#if sentence starts with "then"
	elif sentence[0:5] == 'then ':
		
		#if sentence has "then If"
		if sentence[4:8] == ' If ':
			rootposition.append(position)
			rootvalue.append(len(text))
			te = logiparser(a, position + 1, rootposition, rootvalue, text + ' => ' + sentence[8:-1])
		
		else:
			te = text + ' => ' + sentence[5:] + '\n'
			if (position + 1) < len(a):
				te = logiparser(a, position + 1, rootposition, rootvalue, te)
	
	#if sentence starts with "Otherwise"
	else:
		anteline = a[rootposition[-1]]
		if rootvalue[-1] > 0:
			antecedent = text[0:rootvalue[-1]] + ' => Not' + '(' + anteline[anteline.find('If') + 3:-1] + ')'
		else:
			antecedent = 'Not' + '(' + anteline[anteline.find('If') + 3:-1] + ')'
		rootposition = rootposition[:-1]
		rootvalue = rootvalue[:-1]
		
		#if sentence has "Otherwise: If"
		if sentence[9:13] == ' If ':
			rootposition.append(position)
			rootvalue.append(len(text))
			te = logiparser(a, position + 1, rootposition, rootvalue, text + antecedent + ' => ' + sentence[14:-1])
		
		else:
			te = text + antecedent + ' => ' + sentence[11:] + '\n'
			if (position + 1) < len(a):
				te = logiparser(a, position + 1, rootposition, rootvalue, te)
	return te

def z3parser(text):
	text = text.split('\n')
	rtextarray = []
	rtext = ''
	for texti in text:
		ltexti = len(texti)
		texttoadd = ''
		textindex = 0
		endparen = 0
		while (textindex < ltexti):
			ftexti = texti.find(' => ')
			if ftexti != -1:
				texttoadd = texttoadd + 'Implies(' + texti[0:ftexti] + ', '
				texti = texti[ftexti + 4:]
				textindex = ftexti + 4
				endparen = endparen + 1
			else:
				 texttoadd = texttoadd + texti[0:]
				 for z3j in xrange(endparen):
				 	texttoadd = texttoadd + ')'
				 texttoadd = texttoadd + '\n'
				 textindex = ltexti
		rtext = rtext + texttoadd
	return rtext

#Main code (For ONE function)
#fstr = raw_input('Type the LLVM file you want to verify: ')
#f = open(fstr, 'r')
f = open('examplels.ll', 'r')
k = list(f)
k_start = 0
k_end = k.index('}\n')
c = 0;
variable_names = []
variable_values = []
label_names = []
label_places = []
logictext = ''

#Grab variable names/values, and label names/places
while (k_start < k_end):
	
	#First line: main variables are defined
	#Parse the line properly
	line = k[k_start]
	line = line.strip('\n')
	line = line.strip()
	
	#Get input variable names
	if line[0:7] == 'define ':
		while (line.find('%') != -1):
			if line.find(',') == -1:
				v_name = line[line.find('%'): line.find(')')]
				variable_names.append(v_name)
				variable_values.append(0)
				break
			else:
				v_name = line[line.find('%'): line.find(',')]
				line = line[line.find(',') + 1:]
				variable_names.append(v_name)
				variable_values.append(0)
	
	#Get variable names
	elif ' alloca ' in line:
		v_name = line[0:line[0:].find(' ')]
		variable_names.append(v_name)
		variable_values.append(0)
	
	#Find variable values
	elif line[0:6] == 'store ':
		
		#First find value to add, whether it is string or number
		line1 = line[6:]
		t = line1[line1.find(' ') + 1:line1.find(',')]
		if t.replace('.','',1).isdigit():
			t = int(t)
		
		#Then find variable to store to, then store value to variable
		line1 = line1[line1.find(',') + 2:]
		line1_end = line1.find(',')
		if line1_end != -1:
			to_store = line1[line1.find(' ') + 1:line1_end]
		else:
			to_store = line1[line1.find(' ') + 1:]
		variable_values[variable_names.index(to_store)] = t
	
	#If it hits a label name, grab name and place
	elif line[0:1] == ';' and '<label>' in line:
		label_names.append('%' + line[10:10 + line[10:].find(' ')])
		label_places.append(k_start)
		while (line[0:3] != 'br ') and (k_start < k_end):
			k_start = k_start + 1
			line = k[k_start]
			line = line.strip('\n')
			line = line.strip()
	k_start = k_start + 1

#Loop analyzer
k_start = 0
while (k_start < k_end):
	line = k[k_start]
	line = line.strip('\n')
	line = line.strip()
	
	#If it hits a branch
	if line[0:3] == 'br ':
		if line.find(',') == -1:
			labeltext = line[line.find('label '):]
			labelname = labeltext[labeltext.find(' '):][1:]
			text = ''
			labels = []
			if logictext:
				logictext = logictext + '//\n' + uncloop(k, labelname, labels, text, label_names, label_places, variable_names, variable_values)
			else:
				logictext = uncloop(k, labelname, labels, text, label_names, label_places, variable_names, variable_values)
			
	#If it hits a label name, skip, since labels are taken care of in uncloop and cloop
	elif line[0:1] == ';' and '<label>' in line:
		while (line[0:3] != 'br ') and (k_start < k_end):
			k_start = k_start + 1
			line = k[k_start]
			line = line.strip('\n')
			line = line.strip()
	k_start = k_start + 1

f.close()
logictext = logictext.split('//\n')
for logictextpart in logictext:
	logictextpart = renamer(logictextpart)
	truetext = logiparser(logictextpart, 0, [], [], '')
	print truetext
	truetext = z3parser(truetext)
	print truetext
