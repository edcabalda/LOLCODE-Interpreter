'''
====================================== LOLCODE INTERPRETER ======================================

>>> AUTHOR				:	CABALDA, Elroy Christian D.

>>>	PROGRAM DESCRIPTION :	A program that takes a lolcode file (filename.lol) and performs
							lexical, syntax, and semantic analysis. This program will also run
							the lolcode file. Additionally, this program will display the symbol
							table that was used by the inputted lolcode file. 

>>> FILE DESCRIPTION	: 	This file performs syntax analysis on the lolcode file provided. 
	(syn.py)
'''

import sys
import tkinter as tk

def recasting(stack, cur_index, token_list):

	global valid_flag

	data_type = ["Boolean Type", "Null Type", "Integer Type", "Float Type", "String Type"]
	
	# <recasting> ::= <identifier> IS NOW A <data_type>
	if token_list[cur_index] == "Typecasting_IS_NOW_A":
		cur_index += 1

		if token_list[cur_index] in data_type:
			cur_index += 1

		else:
			console.insert(tk.END, "Syntax Error: Expected Data Type keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False
	else:
		console.insert(tk.END, "Syntax Error: Expected 'Typecasting_IS_NOW_A' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def casting_explicit(stack, cur_index, token_list):

	global valid_flag

	data_type = ["Boolean Type", "Null Type", "Integer Type", "Float Type", "String Type"]

	# <explicit> ::= MAEK <identifier> A <data_type>
	if token_list[cur_index] == "Identifier":
		cur_index += 1

		if token_list[cur_index] == "Typecasting Separator":
			cur_index += 1

			if token_list[cur_index] in data_type:
				cur_index += 1

		elif token_list[cur_index] in data_type:
			cur_index += 1

		else:
			console.insert(tk.END, "Syntax Error: Expected Data Type or 'Typecasting Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	else:
		console.insert(tk.END, "Syntax Error: Expected Identifier keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def concatenation(stack, cur_index, token_list):

	global valid_flag
	
	# <concatenation> ::= SMOOSH <stuffs>
	if token_list[cur_index] == "Concatenation":
		cur_index += 1

		stack, cur_index = expression(stack, cur_index, token_list)

		if valid_flag:
			if token_list[cur_index] == "Variable Separator":
				cur_index += 1

				stack, cur_index = expression(stack, cur_index, token_list)

				while valid_flag and token_list[cur_index] == "Variable Separator":
					cur_index += 1

					stack, cur_index = expression(stack, cur_index, token_list)

			else:
				console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
				valid_flag = False

	return stack, cur_index

def comparison_fxn(stack, cur_index, token_list):

	global valid_flag

	# <comparison> ::= BOTH SAEM <expression> AN <expression>
	if token_list[cur_index] == "Equal":
		cur_index += 1

		stack, cur_index = expression(stack, cur_index, token_list)

		if token_list[cur_index] == "Variable Separator":
			cur_index += 1

			stack, cur_index = expression(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <comparison> ::= DIFFRINT <expression> AN <expression>
	elif token_list[cur_index] == "Not Equal":
		cur_index += 1

		stack, cur_index = expression(stack, cur_index, token_list)

		if token_list[cur_index] == "Variable Separator":
			cur_index += 1

			stack, cur_index = expression(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False
	else:
		console.insert(tk.END, "Syntax Error: Expected 'Equal' or 'Not Equal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def inf_bool_segment(stack, cur_index, token_list):

	global valid_flag
	
	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"] 
	boolean = ["And", "Or", "Xor", "Not"]
	comparison = ["Equal", "Not Equal"]

	if token_list[cur_index] in boolean:
		stack, cur_index = boolean_fxn(stack, cur_index, token_list)

	elif token_list[cur_index] in comparison:
		stack, cur_index = comparison_fxn(stack, cur_index, token_list)

	elif token_list[cur_index] == "Identifier":
		cur_index += 1

		return stack, cur_index
	elif token_list[cur_index] in literals:
		cur_index += 1

	else:
		console.insert(tk.END, "Syntax Error: Expected Boolean or Identifier or Literal keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def inf_bool_fxn(stack, cur_index, token_list):

	global valid_flag

	# <inf_or> ::= ALL OF <stuffs> MKAY 
	if token_list[cur_index] == "Infinite And":
		stack.append(token_list[cur_index])
		
		cur_index += 1
		stack, cur_index = inf_bool_segment(stack, cur_index, token_list) 

		if valid_flag:
			if token_list[cur_index] == "Variable Separator":
				cur_index += 1
				stack, cur_index = inf_bool_segment(stack, cur_index, token_list)
			else:
				console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
				valid_flag = False

			while valid_flag and token_list[cur_index] != "Infinite Delimiter":
				if token_list[cur_index] == "Variable Separator":
					cur_index += 1

					stack, cur_index = inf_bool_segment(stack, cur_index, token_list)

				else:
					console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' or 'Infinite Delimiter' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
					valid_flag = False

			stack_value = stack.pop(len(stack)-1)
			if stack_value != "Infinite And":
				console.insert(tk.END, "Syntax Error: Mismatch of delimiters, expected 'Infinite And'")
				valid_flag = False

			cur_index += 1

	# <inf_or> ::= ANY OF <stuffs> MKAY 
	elif token_list[cur_index] == "Infinite Or":
		stack.append(token_list[cur_index])
		
		cur_index += 1
		stack, cur_index = inf_bool_segment(stack, cur_index, token_list) 

		if valid_flag:
			if token_list[cur_index] == "Variable Separator":
				cur_index += 1
				stack, cur_index = inf_bool_segment(stack, cur_index, token_list)
			else:
				console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
				valid_flag = False

			while valid_flag and token_list[cur_index] != "Infinite Delimiter":
				if token_list[cur_index] == "Variable Separator":
					stack, cur_index = inf_bool_segment(stack, cur_index, token_list)
				else:
					console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
					valid_flag = False

			stack_value = stack.pop(len(stack)-1)
			if stack_value != "Infinite Or":
				console.insert(tk.END, "Syntax Error: Mismatch of delimiters, expected 'Infinite And'")
				valid_flag = False

			cur_index += 1

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Infinite And' or 'Infinite Or' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def next_val(stack, cur_index, token_list):

	global valid_flag

	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"]
	operations = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Maximum", "Minimum", "And", "Or", "Xor", "Not", "Infinite And", "Infinite Or", "Equal", "Not Equal"]

	# <next_val> ::= <stuffs> AN <expressions>
	if token_list[cur_index] == "Variable Separator":
		cur_index += 1

		if token_list[cur_index] == "Identifier":
			cur_index += 1
		
		elif token_list[cur_index] in literals:
			cur_index += 1

		elif token_list[cur_index] in operations:
			stack, cur_index = expression(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' or 'Arithmetic' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Variable Separator' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def boolean_fxn(stack, cur_index, token_list):

	global valid_flag

	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"]
	operations = ["And", "Or", "Xor", "Not"]

	# <boolean> ::= BOTH OF <expression> AN <expression>
	if token_list[cur_index] == "And":
		cur_index += 1

		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in operations:
			stack, cur_index = boolean_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <boolean> ::= EITHER OF <expression> AN <expression>
	elif token_list[cur_index] == "Or":
		cur_index += 1

		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in operations:
			stack, cur_index = boolean_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <boolean> ::= WON OF <expression> AN <expression>
	elif token_list[cur_index] == "Xor":
		cur_index += 1

		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in operations:
			stack, cur_index = boolean_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <boolean> ::= NOT <expression>
	elif token_list[cur_index] == "Not": 
		cur_index += 1

		if token_list[cur_index] == "Identifier":
			cur_index += 1

		elif token_list[cur_index] in literals:
			cur_index += 1

		elif token_list[cur_index] in operations:
			stack, cur_index = boolean_fxn(stack, cur_index, token_list)

		else:
			console.insert(tk,END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	else:
		console.insert(tk,END, "Syntax Error: Expected Boolean keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def arithmetic_fxn(stack, cur_index, token_list):

	global valid_flag
	
	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"] 
	operations = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Maximum", "Minimum"]

	# <arithmetic> ::= SUM OF <expression> AN <expression>
	if token_list[cur_index] == "Addition":
		cur_index += 1

		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in operations:
			stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <arithmetic> ::= DIFF OF <expression> AN <expression>
	elif token_list[cur_index] == "Subtraction":
		cur_index += 1

		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)
		
		elif token_list[cur_index] in operations:
			stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <arithmetic> ::= PRODUKT OF <expression> AN <expression>
	elif token_list[cur_index] == "Multiplication":
		cur_index += 1
		
		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		elif token_list[cur_index] in operations:
			stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <arithmetic> ::= QUOSHUNT OF <expression> AN <expression>
	elif token_list[cur_index] == "Division":
		cur_index += 1
		
		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		elif token_list[cur_index] in operations:
			stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <arithmetic> ::= MOD OF <expression> AN <expression>
	elif token_list[cur_index] == "Modulo":
		cur_index += 1
		
		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		elif token_list[cur_index] in operations:
			stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <arithmetic> ::= BIGGR OF <expression> AN <expression>
	elif token_list[cur_index] == "Maximum":
		cur_index += 1
		
		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		elif token_list[cur_index] in operations:
			stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <arithmetic> ::= SMALLR OF <expression> AN <expression>
	elif token_list[cur_index] == "Minimum":
		cur_index += 1
		
		if token_list[cur_index] == "Identifier":
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)

		elif token_list[cur_index] in literals:
			cur_index += 1
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		elif token_list[cur_index] in operations:
			stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)
			stack, cur_index = next_val(stack, cur_index, token_list)
			
		else:
			console.insert(tk.END, "Syntax Error: Expected 'Identifier' or 'Literal' keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False
	else:
		console.insert(tk.END, "Syntax Error: Expected Arithmetic keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def expression(stack, cur_index, token_list):

	global valid_flag
	
	arithmetic = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Maximum", "Minimum"]
	boolean = ["And", "Or", "Xor", "Not"]
	inf_bool = ["Infinite And", "Infinite Or"]
	comparison = ["Equal", "Not Equal"]
	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"] 

	# <expression> ::= <arithmetic>
	if token_list[cur_index] in arithmetic:
		stack, cur_index = arithmetic_fxn(stack, cur_index, token_list)

	# <expression> ::= <boolean>
	elif token_list[cur_index] in boolean:
		stack, cur_index = boolean_fxn(stack, cur_index, token_list)

	# <expression> ::= <inf_bool>
	elif token_list[cur_index] in inf_bool:
		stack, cur_index = inf_bool_fxn(stack, cur_index, token_list)

	# <expression> ::= <comparison>
	elif token_list[cur_index] in comparison:
		stack, cur_index = comparison_fxn(stack, cur_index, token_list)

	# <expression> ::= <concatenation>
	elif token_list[cur_index] == "Concatenation":
		stack, cur_index = concatenation(stack, cur_index, token_list)

	# <expression> ::= <identifier>
	elif token_list[cur_index] == "Identifier":
		cur_index += 1

	# <expression> ::= <literal>
	elif token_list[cur_index] in literals:
		cur_index += 1

	else:
		console.insert(tk.END, "Syntax Error: Expected Arithmetic or Boolean or Comparison keywords, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def switch_case(stack, cur_index, token_list):

	global valid_flag

	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"]

	# <switch_case> ::= OMG <stuffs>
	if token_list[cur_index] == "Case Block":
		cur_index += 1

		if token_list[cur_index] in literals:
			cur_index += 1

			stack, cur_index = code_block(stack, cur_index, token_list)
			if valid_flag:
				stack, cur_index = switch_case(stack, cur_index, token_list)
		else:
			console.insert(tk.END, "Syntax Error: Expected 'Literal', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <switch_case> ::= OMGWTF <stuffs>
	elif token_list[cur_index] == "Default Block":
		cur_index += 1

		stack, cur_index = code_block(stack, cur_index, token_list)
		if valid_flag:
			stack, cur_index = switch_case(stack, cur_index, token_list)
	
	# <switch_case> ::= <stuffs> OIC
	elif token_list[cur_index] == "Control Flow Delimiter End":
		stack_value = stack.pop(len(stack)-1)

		# checks if the delimiters match
		if stack_value == "Switch-Case Delimiter Start":
			# update the index
			cur_index += 1
		else:
			console.insert(tk.END, "Syntax Error: Mismatch of delimiters, expected 'Switch-Case Delimiter Start'")
			valid_flag = False

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Else If Block' or 'Else Block', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index 

def if_then(stack, cur_index, token_list):
	global valid_flag

	# <if_then> ::= YA RLY <stuffs>
	if token_list[cur_index] == "If Block":
		cur_index += 1

		stack, cur_index = code_block(stack, cur_index, token_list)
		if valid_flag and cur_index < len(token_list):
			stack, cur_index = if_then(stack, cur_index, token_list)

	# <if_then> ::= NO WAI <stuffs>
	elif token_list[cur_index] == "Else Block":
		cur_index += 1

		stack, cur_index = code_block(stack, cur_index, token_list)
		if valid_flag and cur_index < len(token_list):
			stack, cur_index = if_then(stack, cur_index, token_list)
	
	# <if_then> ::= <stuffs> OIC
	elif token_list[cur_index] == "Control Flow Delimiter End":
		stack_value = stack.pop(len(stack)-1)

		# checks if the delimiters match
		if stack_value == "If-Then Delimiter Start":
			# update the index
			cur_index += 1

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Else Block', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def loop_cond(stack, cur_index, token_list):

	global valid_flag

	# <loop_cond> ::= TIL <expression>
	if token_list[cur_index] == "Until":
		cur_index += 1

		stack, cur_index = expression(stack, cur_index, token_list)

		stack, cur_index = code_block(stack, cur_index, token_list)

	# <loop_cond> ::= WILE <expression>
	elif token_list[cur_index] == "While":
		cur_index += 1

		stack, cur_index = expression(stack, cur_index, token_list)

		stack, cur_index = code_block(stack, cur_index, token_list)

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Until' or 'While', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def loop_op(stack, cur_index, token_list):

	global valid_flag

	# <loop_op> ::= UPPIN YR <identifier> <stuffs>
	if token_list[cur_index] == "Increment":
		cur_index += 1

		if token_list[cur_index] == "Loop Reference":
			cur_index += 1

			if token_list[cur_index] == "Identifier":
				cur_index += 1

				stack, cur_index = loop_cond(stack, cur_index, token_list)

			else:
				console.insert(tk.END, "Syntax Error: Expected 'Identifier', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
				valid_flag = False

		else:
			console.insert(tk.END, "Syntax Error: Expected 'Loop Reference', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False

	# <loop_op> ::= NERFIN YR <identifier> <stuffs>
	elif token_list[cur_index] == "Decrement":
		cur_index += 1

		if token_list[cur_index] == "Loop Reference":
			cur_index += 1

			if token_list[cur_index] == "Identifier":
				cur_index += 1
				
				stack, cur_index = loop_cond(stack, cur_index, token_list)

			else:
				console.insert(tk.END, "Syntax Error: Expected 'Identifier', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
				valid_flag = False
		else:
			console.insert(tk.END, "Syntax Error: Expected 'Loop Reference', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False
		
	else:
		console.insert(tk.END, "Syntax Error: Expected 'Increment' or 'Decrement', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def looping(stack, cur_index, token_list):

	global valid_flag

	# <looping> = IM IN YR loopident <loop_op> YR varident <loop_cond> <expr> <code_block> IM OUTTA YR loopident
	if token_list[cur_index] == "Identifier":
		cur_index += 1

		stack, cur_index = loop_op(stack, cur_index, token_list)

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Identifier', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False

	return stack, cur_index

def assignment(stack, cur_index, token_list):

	global valid_flag

	# <assignment> ::= <identifier> R <expr>
	if token_list[cur_index] == "Variable Assignment":
		cur_index += 1

		# <reassignment> ::= <identifier> R <explicit>
		if token_list[cur_index] == "Typecasting_MAEK":
			cur_index += 1
			stack, cur_index = casting_explicit(stack, cur_index, token_list)
		else:
			stack, cur_index = expression(stack, cur_index, token_list)

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Variable Assignment', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False
	
	return stack, cur_index

def inputing(stack, cur_index, token_list):
	global valid_flag

	# <input> ::= GIMMEH <identifier>
	if token_list[cur_index] == "Identifier":
		cur_index += 1
	else:
		console.insert(tk.END, "Syntax Error: Expected 'Identifier', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False
	return stack, cur_index

def declaration_init(stack, cur_index, token_list):

	global valid_flag

	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"]
	arithmetic = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Maximum", "Minimum"]
	boolean = ["And", "Or", "Xor", "Not"]
	inf_bool = ["Infinite And", "Infinite Or"]
	comparison = ["Equal", "Not Equal"]

	# <declaration> ::= I HAS A <identifier> ITZ <literals>
	if token_list[cur_index] in literals:
		cur_index += 1
	# <declaration> ::= I HAS A <identifier> ITZ <identifier>
	elif token_list[cur_index] == "Identifier":
		cur_index += 1
	# <declaration> ::= I HAS A <identifier> ITZ <expressions>
	elif token_list[cur_index] in arithmetic:
		stack, cur_index = expression(stack, cur_index, token_list)
	elif token_list[cur_index] in boolean:
		stack, cur_index = expression(stack, cur_index, token_list)
	elif token_list[cur_index] in inf_bool:
		stack, cur_index = expression(stack, cur_index, token_list)
	elif token_list[cur_index] in comparison:
		stack, cur_index = expression(stack, cur_index, token_list)
	else:
		console.insert(tk.END, "Syntax Error: Expected Literal or Identifier or Expression, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False
	return stack, cur_index		

def declaration(stack, cur_index, token_list):

	global valid_flag

	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"]

	# <declaration> ::= I HAS A <identifier>
	if token_list[cur_index] == "Identifier":
		cur_index += 1

		# if variable is also initialized
		if token_list[cur_index] == "Variable Initialization":
			cur_index += 1
			stack, cur_index = declaration_init(stack, cur_index, token_list)
		
		# accepts ONLY variable declaration without initialization
		return stack, cur_index

	else:
		console.insert(tk.END, "Syntax Error: Expected Identifier, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False
		return stack, cur_index

def printing(stack, cur_index, token_list, line_print):

	global valid_flag

	literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"]
	operations = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Maximum", "Minimum", "And", "Or", "Xor", "Not", "Infinite And", "Infinite Or", "Equal", "Not Equal", "Concatenation"]
	
	# if printing in the same line
	if valid_flag and line_nums[cur_index] == line_print:
		
		# <printing> ::= VISIBLE <literal>
		if token_list[cur_index] in literals:
			cur_index += 1

			if token_list[cur_index] in literals:
				stack, cur_index = printing(stack, cur_index, token_list, line_print)
			elif token_list[cur_index] == "Identifier":
				stack, cur_index = printing(stack, cur_index, token_list, line_print)
			elif token_list[cur_index] in operations:
				stack, cur_index = expression(stack, cur_index, token_list)
				stack, cur_index = printing(stack, cur_index, token_list, line_print)

		# <printing> ::= VISIBLE <identifier>
		elif token_list[cur_index] == "Identifier":
			cur_index += 1

			if token_list[cur_index] in literals:
				stack, cur_index = printing(stack, cur_index, token_list, line_print)
			elif token_list[cur_index] == "Identifier":
				stack, cur_index = printing(stack, cur_index, token_list, line_print)
			elif token_list[cur_index] in operations:
				stack, cur_index = expression(stack, cur_index, token_list)
				stack, cur_index = printing(stack, cur_index, token_list, line_print)

		# <printing> ::= VISIBLE <expressions>
		elif token_list[cur_index] in operations:
			stack, cur_index = expression(stack, cur_index, token_list)
			stack, cur_index = printing(stack, cur_index, token_list, line_print)

		else:
			console.insert(tk.END, "Syntax Error: Expected Literal or Identifier, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
			valid_flag = False
		
	return stack, cur_index

def code_block(stack, cur_index, token_list):
	global valid_flag

	# if index out of bounds, return
	if cur_index >= len(token_list):
		return stack, cur_index
	
	# <code_block> ::= <printing>
	if token_list[cur_index] == "Output Keyword":

		# update the index
		cur_index += 1
		line_print = line_nums[cur_index]
		# go to the next production rule
		stack, cur_index = printing(stack, cur_index, token_list, line_print)
		
		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <code_block> ::= <declaration>
	elif token_list[cur_index] == "Variable Declaration":

		# update the index
		cur_index += 1
		# go to the next production rule
		stack, cur_index = declaration(stack, cur_index, token_list)

		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <code_block> ::= <input>
	elif token_list[cur_index] == "Input Keyword":

		# update the index
		cur_index += 1
		# go to the next production rule
		stack, cur_index = inputing(stack, cur_index, token_list)

		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <code_block> ::= <assignment>
	# <code_block> ::= <recasting> 
	elif token_list[cur_index] == "Identifier":

		# update the index
		cur_index += 1
		# go to the next production rule 
		if token_list[cur_index] == "Variable Assignment":
			stack, cur_index = assignment(stack, cur_index, token_list)
		elif token_list[cur_index] == "Typecasting_IS_NOW_A":
			stack, cur_index = recasting(stack, cur_index, token_list)
		
		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <code_block> ::= <looping>
	elif token_list[cur_index] == "Loop Delimiter Start":

		# append the delimiter to the stack
		stack.append(token_list[cur_index])
		# update the index
		cur_index += 1
		# go to the next production rule
		stack, cur_index = looping(stack, cur_index, token_list)

		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <code_block> ::= <if>
	elif token_list[cur_index] == "If-Then Delimiter Start":

		# append the delimiter to the stack
		stack.append(token_list[cur_index])
		# update the index
		cur_index += 1
		# go to the next production rule
		stack, cur_index = if_then(stack, cur_index, token_list)

		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <code_block> ::= <switch>
	elif token_list[cur_index] == "Switch-Case Delimiter Start":

		# append the delimiter to the stack
		stack.append(token_list[cur_index])
		# update the index
		cur_index += 1
		# go to the next production rule
		stack, cur_index = switch_case(stack, cur_index, token_list)

		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <code_block> :: = <explicit>
	elif token_list[cur_index] == "Typecasting_MAEK":
		# update the index
		cur_index += 1
		# go to the next production rule
		stack, cur_index = casting_explicit(stack, cur_index, token_list)

		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)
		return stack, cur_index

	# <program> ::= HAI <code_block> KTHXBYE
	elif token_list[cur_index] == "Code Delimiter End":

		# update the index
		cur_index += 1
		stack_value = stack.pop(len(stack)-1)

		# checks if the delimiters match
		if stack_value != "Code Delimiter Start":
			console.insert(tk.END, "Syntax Error: Mismatch of delimiters, expected 'Code Delimiter Start', got '" + stack_value + "'")
			valid_flag = False

		return stack, cur_index

	# <code_block> ::= IM IN YR <stuffs> IM OUTTA YR
	elif token_list[cur_index] == "Loop Delimiter End":

		# update the index
		cur_index += 1
		stack_value = stack.pop(len(stack)-1)

		# checks if the delimiters match
		if stack_value != "Loop Delimiter Start":
			console.insert(tk.END, "Syntax Error: Mismatch of delimiters, expected 'Loop Delimiter Start', got '" + stack_value + "'")
			valid_flag = False

		else:

			# gets the closing identifier of the loop 
			if token_list[cur_index] == "Identifier":
				cur_index += 1

			else:
				console.insert(tk.END, "Syntax Error: Expected 'Identifier' keyword, got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
				valid_flag = False

		return stack, cur_index

	elif token_list[cur_index] == "Else Block":
		return stack, cur_index

	# <if_then> ::= O RLY? <stuffs> OIC
	# <switch_case> ::= WTF? <stuffs> OIC
	elif token_list[cur_index] == "Control Flow Delimiter End":
		return stack, cur_index

	# <case_block> ::= OMG <stuffs> GTFO
	elif token_list[cur_index] == "Switch-Case Block Break":
		cur_index += 1

		return stack, cur_index 

	# <code_block> ::= <expression>
	else:
		stack, cur_index = expression(stack, cur_index, token_list)

		if valid_flag:
			stack, cur_index = code_block(stack, cur_index, token_list)

		return stack, cur_index

def program(stack, cur_index, token_list):
	global valid_flag
	
	if token_list[cur_index] == "Code Delimiter Start":

		# append the delimiter to the stack
		stack.append(token_list[cur_index])
		# update index
		cur_index += 1

		# go to the next production rule
		stack, cur_index = code_block(stack, cur_index, token_list)

		return stack, cur_index

	else:
		console.insert(tk.END, "Syntax Error: Expected 'Code Delimiter Start', got '" + token_list[cur_index] + "' in line number " + line_nums[cur_index])
		valid_flag = False
		return stack, cur_index

def syntax(symbol_table, console_window):
	
	global line_nums
	line_nums = []

	global console
	console = console_window

	global valid_flag
	valid_flag = True
	
	# gets all the token types of the symbol table
	token_list = []
	for lexeme in symbol_table:
		token_list.append(lexeme[1])
		line_nums.append(str(lexeme[2]))

	# initializing the stack and the current index
	stack = []
	cur_index = 0
	
	stack, cur_index = program(stack, cur_index, token_list)

	if not valid_flag:
		return False
	elif len(stack) != 0:
		console.insert(tk.END, "Syntax Error: Unmatched Delimiter '" + stack[len(stack)-1] + "'")
		return False
	else:
		return True
