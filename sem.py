'''
====================================== LOLCODE INTERPRETER ======================================

>>> AUTHOR				:	CABALDA, Elroy Christian D.

>>>	PROGRAM DESCRIPTION :	A program that takes a lolcode file (filename.lol) and performs
							lexical, syntax, and semantic analysis. This program will also run
							the lolcode file. Additionally, this program will display the symbol
							table that was used by the inputted lolcode file. 

>>> FILE DESCRIPTION	: 	This file performs semantic analysis on the lolcode file provided. 
	(sem.py)
'''

import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk

literals = ["Integer Literal", "Float Literal", "String Literal", "True", "False"]
operations = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Maximum", "Minimum", "And", "Or", "Xor", "Not", "Infinite And", "Infinite Or", "Equal", "Not Equal", "Concatenation"]
arithmetic = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo", "Maximum", "Minimum"]
boolean = ["And", "Or", "Xor", "Not"]
inf_bool = ["Infinite And", "Infinite Or"]
comparison = ["Equal", "Not Equal"]

def modify_variable(variable, operation):

	# gets the value of the variable to be modified
	value = get_value(variable)

	# if the operation is increment, add 1
	if operation == "Increment":
		value += 1
	# if the operation is decrement, subtract 1
	elif operation == "Decrement":
		value -= 1

	# update the value of the variable
	ent_type = check_type(value)
	put_value(variable, value, ent_type)

def assess_condition(symbol_table, variable, start, end):

	# while the value of the expression is not yet assessed
	while start < end:
		start, value = expressions(symbol_table, start)

	# returns the result
	if value == "WIN":
		return True
	else:
		return False

def get_loop_expression(symbol_table, cur_index, line_num):
	# returns the index of the last part of the expression to assess
	while symbol_table[cur_index][2] == line_num:
		cur_index += 1
	return cur_index

def loop_decode(symbol_table, cur_index):

	# gets the loop identifier
	loop_ident = symbol_table[cur_index][0]
	cur_index += 1

	# gets the loop operation
	loop_op = symbol_table[cur_index][1]
	cur_index += 2

	# gets the variable identifier to be modified
	mod_variable = symbol_table[cur_index][0]
	cur_index += 1

	# gets the loop condition
	loop_cond = symbol_table[cur_index][1]
	cur_index += 1

	# gets the expression to assess
	line_num = symbol_table[cur_index][2]
	expr_start_index = cur_index
	expr_end_index = get_loop_expression(symbol_table, cur_index, line_num)
	cur_index = expr_end_index

	return cur_index, loop_ident, loop_op, mod_variable, loop_cond, expr_start_index, expr_end_index

def looping(symbol_table, cur_index):
	global valid_flag
	# gets the notable info from the loop declaration line
	cur_index, loop_ident, loop_op, mod_variable, loop_cond, expr_start_index, expr_end_index = loop_decode(symbol_table, cur_index)

	# take note of the loop identifier
	loop_stack.append(loop_ident)
	# take note of where the loop starts
	loop_restart = cur_index

	# if the loop condition is While
	if loop_cond == "Until":
		satisfy_condition = assess_condition(symbol_table, mod_variable, expr_start_index, expr_end_index)
		
		# condition must be False to continue looping
		while satisfy_condition == False:
			# go back to the start of the loop
			cur_index = loop_restart
			
			# execute the code blocks until the delimiter is encountered
			while symbol_table[cur_index][1] != "Loop Delimiter End":
				cur_index = code_block(symbol_table, cur_index)
			
			# modify the variable depending on the operation
			modify_variable(mod_variable, loop_op)
			# update the condition
			satisfy_condition = assess_condition(symbol_table, mod_variable, expr_start_index, expr_end_index)
		
		cur_index += 1
		loop_ident = symbol_table[cur_index][0]
		stack_value = loop_stack.pop(len(loop_stack)-1)

		# once the loop is finished, check if the identifiers for the loop match
		if loop_ident != stack_value:
			console.insert(tk.END, "Semantic Error: Wrong loop identifier '" + stack_value + "', expected loop identifier '" + loop_ident + "'")
			
			valid_flag = False
		
		cur_index += 1
		return cur_index

	# if the loop condition is While
	elif loop_cond == "While":
		satisfy_condition = assess_condition(symbol_table, mod_variable, expr_start_index, expr_end_index)
		
		# condition must be True to continue looping
		while satisfy_condition == True:
			# go back to the start of the loop
			cur_index = loop_restart
			
			# execute the code blocks until the delimiter is encountered
			while symbol_table[cur_index][1] != "Loop Delimiter End":
				cur_index = code_block(symbol_table, cur_index)
			
			# modify the variable depending on the operation
			modify_variable(mod_variable, loop_op)
			# update the condition
			satisfy_condition = assess_condition(symbol_table, mod_variable, expr_start_index, expr_end_index)
		
		
		cur_index += 1
		loop_ident = symbol_table[cur_index][0]
		stack_value = loop_stack.pop(len(loop_stack)-1)

		# once the loop is finished, check if the identifiers for the loop match 
		if loop_ident != stack_value:
			console.insert(tk.END, "Semantic Error: Wrong loop identifier '" + stack_value + "', expected loop identifier '" + loop_ident + "'")
			
			valid_flag = False
		
		cur_index += 1
		return cur_index

def switch_case(symbol_table, cur_index):

	# gets the value of implicit variable IT
	it_value = get_value(new_table[0][0])

	# if a case block is encountered
	if cur_index < len(symbol_table) and symbol_table[cur_index][1] == "Case Block":
		cur_index += 1
		case_value = symbol_table[cur_index][0]
		cur_index += 1

		# check if the value of IT and the case block is equal
		if it_value == case_value:
			# execute the code blocks until the block break is encountered
			while cur_index < len(symbol_table) and symbol_table[cur_index][1] != "Switch-Case Block Break":
				cur_index = code_block(symbol_table, cur_index)
			# go to the end of the switch-case block
			while symbol_table[cur_index][1] != "Control Flow Delimiter End":
				cur_index += 1
			return cur_index

		# else continue until the block break is encountered
		else:
			while cur_index < len(symbol_table) and symbol_table[cur_index][1] != "Switch-Case Block Break":
				cur_index += 1

			# assess the next block
			cur_index += 1
			cur_index = switch_case(symbol_table, cur_index)
			return cur_index

	# if the default block is encountered
	elif cur_index < len(symbol_table) and  symbol_table[cur_index][1] == "Default Block":
		# execute the code blocks until the delimiter is encountered
		while symbol_table[cur_index][1] != "Control Flow Delimiter End":
			cur_index = code_block(symbol_table, cur_index)
		return cur_index

	else:
		return cur_index

def if_then(symbol_table, cur_index):

	# gets the value of implicit variable IT
	it_value = get_value(new_table[0][0])
	it_value = typecasting_bool(it_value)

	cur_index += 1

	# if IT is True
	if it_value:
		# execute the code blocks until an else block or the delimiter is encountered
		while symbol_table[cur_index][1] != "Else Block" and symbol_table[cur_index][1] != "Control Flow Delimiter End":
			cur_index = code_block(symbol_table, cur_index)
		# go to the end of the if-then block
		while symbol_table[cur_index][1] != "Control Flow Delimiter End":
			cur_index += 1
		return cur_index
	else:
		# skip the code blocks until the else block is encountered
		while symbol_table[cur_index][1] != "Else Block":
			cur_index += 1 
		# execute the code blocks until the delimiter is encountered
		while symbol_table[cur_index][1] != "Control Flow Delimiter End":
			cur_index = code_block(symbol_table, cur_index)
		return cur_index

def typecasting(symbol_table, cur_index, identifier):
	global valid_flag
	# casting to integer
	if symbol_table[cur_index][1] == "Integer Type":
		value = get_value(identifier)
		try:
			value = int(value)
		except ValueError:
			console.insert(tk.END, "Semantic Error: Cannot typecast '" + str(value) + "' into a NUMBR")
			
			valid_flag = False

	# casting to float
	elif symbol_table[cur_index][1] == "Float Type":
		value = get_value(identifier)
		try:
			value = float(value)
		except ValueError:
			console.insert(tk.END, "Semantic Error: Cannot typecast '" + str(value) + "' into a NUMBR") 
			
			valid_flag = False

	# casting to string
	elif symbol_table[cur_index][1] == "String Type":
		value = get_value(identifier)
		try:
			value = str(value)
		except ValueError:
			console.insert(tk.END, "Semantic Error: Cannot typecast '" + str(value) + "' into a NUMBR") 
			
			valid_flag = False

	# casting to boolean
	elif symbol_table[cur_index][1] == "Boolean Type":
		value = get_value(identifier)
		if value == "" or value == 0 or value == 0.0 or value == "NOOB":
			value = "FAIL"
		else:
			value = "WIN"

	elif symbol_table[cur_index][1] == "Null Type":
		console.insert(tk.END, "Semantic Error: Typecasting into NOOB is not allowed")
		
		valid_flag = False

	return cur_index, value

def recasting(symbol_table, cur_index, identifier):
	cur_index, value = typecasting(symbol_table, cur_index, identifier)

	# updates the value of the identifier
	ent_type = check_type(value)
	put_value(identifier, value, ent_type)

	cur_index += 1
	return cur_index

def explicit_typecasting(symbol_table, cur_index):
	identifier = symbol_table[cur_index][0]
	cur_index += 1

	# if there is an optional Typecasting Separator present
	if symbol_table[cur_index][1] == "Typecasting Separator":
		cur_index += 1

	cur_index, value = typecasting(symbol_table, cur_index, identifier)

	cur_index += 1
	return cur_index, value

def concatenation(symbol_table, cur_index):
	line_num = symbol_table[cur_index][2]
	string = ""

	# concatenates all of the expressions in the line
	while symbol_table[cur_index][2] == line_num:
		if symbol_table[cur_index][1] == "Infinite Delimiter":
			cur_index += 1
			return cur_index, string

		elif symbol_table[cur_index][1] == "Variable Separator":
			cur_index += 1

		elif symbol_table[cur_index][1] in literals:
			append = str(symbol_table[cur_index][0])
			string = string + append
			cur_index += 1

		elif symbol_table[cur_index][1] == "Identifier":
			temp = get_value(symbol_table[cur_index][0])
			append = str(temp)
			string = string + append
			cur_index += 1

		elif symbol_table[cur_index][1] in operations:
			cur_index, temp = expressions(symbol_table, cur_index)
			append = str(temp)
			string = string + append

	# returns the concatenated string
	return cur_index, string

def typecasting_comparison(value):
	# try to cast to int
	try:
		value = int(value)
	except ValueError:
		# try to cast to float
		try:
			value = float(value)
		except ValueError:
			global valid_flag
			console.insert(tk.END, "Semantic Error: Cannot typecast '" + str(value) + "' into a NUMBR or NUMBAR")
			
			valid_flag = False
	return value

def comparison_fxn(symbol_table, cur_index):
	global valid_flag

	if symbol_table[cur_index][1] == "Equal":
		cur_index += 1

		# gets value of 3rd operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in operations:
			cur_index, value1 = expressions(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in operations:
			cur_index, value2 = expressions(symbol_table, cur_index)

		# typecasting values to something comparable
		if valid_flag:
			value1 = typecasting_comparison(value1)
		if valid_flag:
			value2 = typecasting_comparison(value2)
		
		# returns the TROOF equivalent
		if valid_flag:
			if value1 == value2:
				value = "WIN"
			else:
				value = "FAIL"
		else:
			value = None

		return cur_index, value

	# if the comparison operation is Not Equal
	elif symbol_table[cur_index][1] == "Not Equal":
		cur_index += 1

		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in operations:
			cur_index, value1 = expressions(symbol_table, cur_index)
			cur_index += 1

		# gets the value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in operations:
			cur_index, value2 = expressions(symbol_table, cur_index)

		# typecasting values to something comparable
		if valid_flag:
			value1 = typecasting_comparison(value1)
		if valid_flag:
			value2 = typecasting_comparison(value2)
		
		# returns the TROOF equivalent
		if valid_flag:
			if value1 == value2:
				value = "WIN"
			else:
				value = "FAIL"
		else:
			value = None

		return cur_index, value
		
def typecasting_bool(value):
	# typecasts literals into their boolean equivalent
	if value == "FAIL" or value == "" or value == 0 or value == 0.0 or value == "NOOB":
		return False
	else:
		return True

def inf_bool_fxn(symbol_table, cur_index):
	global valid_flag
	# if the operation is Infinite Arity And
	if symbol_table[cur_index][1] == "Infinite And":
		cur_index += 1
		
		# gets initial value
		if symbol_table[cur_index][1] == "Identifier":
			value = get_value(symbol_table[cur_index][0])
			value = typecasting_bool(value)
			cur_index += 1
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value = boolean_fxn(symbol_table, cur_index)
			value = typecasting_bool(value)
		elif symbol_table[cur_index][1] in comparison:
			cur_index, value = comparison_fxn(symbol_table, cur_index)
			value = typecasting_bool(value)
		elif symbol_table[cur_index][1] == "FAIL" or symbol_table[cur_index][1] == "" or symbol_table[cur_index][1] == 0 or symbol_table[cur_index][1] == 0.0 or symbol_table[cur_index][1] == "NOOB":
			value = False
			cur_index += 1
		else:
			value = True
			cur_index += 1

		# performs the AND operation to the succeeding values until a delimiter is reached
		while valid_flag and symbol_table[cur_index][1] != "Infinite Delimiter":
			if symbol_table[cur_index][1] == "Variable Separator":
				cur_index += 1

			elif symbol_table[cur_index][1] in literals:
				temp = typecasting_bool(symbol_table[cur_index][0])
				value = value and temp
				cur_index += 1

			elif symbol_table[cur_index][1] == "Identifier":
				temp  = get_value(symbol_table[cur_index][0])
				temp = typecasting_bool(temp)
				value = value and temp
				cur_index += 1

			elif symbol_table[cur_index][1] in boolean:
				cur_index, temp = boolean_fxn(symbol_table, cur_index)
				temp = typecasting_bool(temp)
				value = value and temp

			elif symbol_table[cur_index][1] in comparison:
				cur_index, temp = comparison_fxn(symbol_table, cur_index)
				temp = typecasting_bool(temp)
				value = value and temp

	# if the operation is Infinite Arity Or
	elif symbol_table[cur_index][1] == "Infinite Or":
		cur_index += 1
		
		# gets initial value
		if symbol_table[cur_index][1] == "Identifier":
			value = get_value(symbol_table[cur_index][0])
			value = typecasting_bool(value)
			cur_index += 1
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value = boolean_fxn(symbol_table, cur_index)
			value = typecasting_bool(value)
		elif symbol_table[cur_index][1] in comparison:
			cur_index, value = comparison_fxn(symbol_table, cur_index)
		elif symbol_table[cur_index][1] == "FAIL" or symbol_table[cur_index][1] == "" or symbol_table[cur_index][1] == 0 or symbol_table[cur_index][1] == 0.0 or symbol_table[cur_index][1] == "NOOB":
			value = False
			cur_index += 1
		else:
			value = True
			cur_index += 1

		# performs the OR operation to the succeeding values until a delimiter is reached 
		while valid_flag and symbol_table[cur_index][1] != "Infinite Delimiter":
			if symbol_table[cur_index][1] == "Variable Separator":
				cur_index += 1

			elif symbol_table[cur_index][1] in literals:
				temp = typecasting_bool(symbol_table[cur_index][0])
				value = value or temp
				cur_index += 1

			elif symbol_table[cur_index][1] == "Identifier":
				temp  = get_value(symbol_table[cur_index][0])
				temp = typecasting_bool(temp)
				value = value or temp
				cur_index += 1

			elif symbol_table[cur_index][1] in boolean:
				cur_index, temp = boolean_fxn(symbol_table, cur_index)
				temp = typecasting_bool(temp)
				value = value or temp

			elif symbol_table[cur_index][1] in comparison:
				cur_index, temp = comparison_fxn(symbol_table, cur_index)
				temp = typecasting_bool(temp)
				value = value or temp

	cur_index += 1

	# returns the TROOF equivalent
	if valid_flag:
		if value:
			value = "WIN"
		else:
			value = "FAIL"
	else:
		value = None

	return cur_index, value

def boolean_fxn(symbol_table, cur_index):
	global valid_flag
	# if the boolean function is And
	if symbol_table[cur_index][1] == "And":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value1 = boolean_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value2 = boolean_fxn(symbol_table, cur_index)

		# typcasting values to boolean
		if valid_flag:
			value1 = typecasting_bool(value1)
		if valid_flag:
			value2 = typecasting_bool(value2)

		# performs the AND operation
		if valid_flag:
			value = value1 and value2

		# returns the TROOF equivalent
		if valid_flag:
			if value:
				value = "WIN"
			else:
				value = "FAIL"
		else:
			value = None

		return cur_index, value

	# if the boolean function is Or
	elif symbol_table[cur_index][1] == "Or":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value1 = boolean_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value2 = boolean_fxn(symbol_table, cur_index)

		# typcasting the values to boolean
		if valid_flag:
			value1 = typecasting_bool(value1)
		if valid_flag:
			value2 = typecasting_bool(value2)

		# performs the OR operation
		if valid_flag:
			value = value1 or value2

		# return the TROOF equivalent
		if valid_flag:
			if value:
				value = "WIN"
			else:
				value = "FAIL"
		else:
			value = None

		return cur_index, value

	# if the boolean function is Xor
	elif symbol_table[cur_index][1] == "Xor":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value1 = boolean_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value2 = boolean_fxn(symbol_table, cur_index)

		# typcasting the values to boolean
		if valid_flag:
			value1 = typecasting_bool(value1)
		if valid_flag:
			value2 = typecasting_bool(value2)

		# perform the XOR operation
		if valid_flag:
			value = (value1 and not value2) or (not value1 and value2)

		# return the TROOF equivalent
		if valid_flag:
			if value:
				value = "WIN"
			else:
				value = "FAIL"
		else:
			value = None
		
		return cur_index, value

	# if the boolean function is Not
	elif symbol_table[cur_index][1] == "Not":
		cur_index += 1
		
		# get value of the operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in boolean:
			cur_index, value1 = boolean_fxn(symbol_table, cur_index)

		# typcasting the value to boolean
		if valid_flag:
			value1 = typecasting_bool(value1)

		# perform the NOT operation
		if valid_flag:
			value = not value1

		# return the TROOF equivalent
		if valid_flag:
			if value:
				value = "WIN"
			else:
				value = "FAIL"
		else:
			value = None
		
		return cur_index, value

def typcasting_arithmetic(value1, value2):
	global valid_flag
	# try typecasting into int
	try:
		value1 = int(value1)
		value2 = int(value2)
	except ValueError:

		# try typecasting to float
		try:
			value1 = float(value1)
			value2 = float(value2)
		except ValueError:
			typcasted_flag = False

			# try typcasting BOOL to INT
			if value1 == "WIN":
				value1 = 1
			elif value1 == "FAIL":
				value1 = 0
			else:
				console.insert(tk.END, "Semantic Error: Cannot typcast '" + str(value1) + "' into NUMBR or NUMBAR")
				
				valid_flag = False
				value1 = None
			
			# try typcasting BOOL to INT
			if valid_flag:
				if value2 == "WIN":
					value2 = 1
				elif value2 == "FAIL":
					value2 = 0
				else:
					console.insert(tk.END, "Semantic Error: Cannot typcast '" + str(value2) + "' into NUMBR or NUMBAR")
					
					valid_flag = False
					value2 = None
			else:
				valid_flag = False
				value2 = None

	return value1, value2

def arithmetic_fxn(symbol_table, cur_index):
	global valid_flag
	# if the arithmetic function is Addition
	if symbol_table[cur_index][1] == "Addition":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value1 = arithmetic_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value2 = arithmetic_fxn(symbol_table, cur_index)

		# typecasting the values to something that can be computed
		if valid_flag:
			value1, value2 = typcasting_arithmetic(value1, value2)

		# returns the result of the addition operation
		if valid_flag:
			value = value1 + value2
		else:
			value = None
		return cur_index, value

	# if the arithmetic function is Subtraction
	elif symbol_table[cur_index][1] == "Subtraction":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value1 = arithmetic_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value2 = arithmetic_fxn(symbol_table, cur_index)

		# typecasting the values to something that can be computed
		if valid_flag:
			value1, value2 = typcasting_arithmetic(value1, value2)

		# returns the result of the subtraction operation
		if valid_flag:
			value = value1 - value2
		else:
			value = None
		return cur_index, value

	# if the arithmetic function is Multiplication
	elif symbol_table[cur_index][1] == "Multiplication":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value1 = arithmetic_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value2 = arithmetic_fxn(symbol_table, cur_index)

		# typecasting the values to something that can be computed
		if valid_flag:
			value1, value2 = typcasting_arithmetic(value1, value2)

		# returns the result of the multiplication operation
		if valid_flag:
			value = value1 * value2
		else:
			value = None
		return cur_index, value

	# if the arithmetic function is Division
	elif symbol_table[cur_index][1] == "Division":
		cur_index += 1
		
		# gets the value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value1 = arithmetic_fxn(symbol_table, cur_index)
			cur_index += 1


		# gets the value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value2 = arithmetic_fxn(symbol_table, cur_index)

		# typecasting the values to something that can be computed
		if valid_flag:
			value1, value2 = typcasting_arithmetic(value1, value2)

		# if one of the values is float, do float division
		if valid_flag:
			if type(value1) == float or type(value1) == float:
				value = value1 / value2
			# else do integer division
			else:
				value = value1 // value2
		else:
			value = None
		
		# returns the result of the division operation 
		return cur_index, value

	# if the arithmetic function is Modulo
	elif symbol_table[cur_index][1] == "Modulo":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value1 = arithmetic_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value2 = arithmetic_fxn(symbol_table, cur_index)

		# typecasting the values to something that can be computed
		if valid_flag:
			value1, value2 = typcasting_arithmetic(value1, value2)

		# returns the result of the modulo operation
		if valid_flag:
			value = value1 % value2
		else:
			value = None
		return cur_index, value

	# if the arithmetic function is Maximum
	elif symbol_table[cur_index][1] == "Maximum":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value1 = arithmetic_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value2 = arithmetic_fxn(symbol_table, cur_index)

		# typecasting the values to something that can be computed
		if valid_flag:
			value1, value2 = typcasting_arithmetic(value1, value2)

		# compares the two values and returns the lower value
		if valid_flag:
			if value1 > value2:
				return cur_index, value1
			else:
				return cur_index, value2
		else:
			return cur_index, None

	# if the arithmetic function is Minimum
	elif symbol_table[cur_index][1] == "Minimum":
		cur_index += 1
		
		# gets value of 1st operand
		if symbol_table[cur_index][1] in literals:
			value1 = symbol_table[cur_index][0]
			cur_index += 2
		elif symbol_table[cur_index][1] == "Identifier":
			value1 = get_value(symbol_table[cur_index][0])
			cur_index += 2
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value1 = arithmetic_fxn(symbol_table, cur_index)
			cur_index += 1

		# gets value of 2nd operand
		if symbol_table[cur_index][1] in literals:
			value2 = symbol_table[cur_index][0]
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			value2 = get_value(symbol_table[cur_index][0])
			cur_index += 1
		elif symbol_table[cur_index][1] in arithmetic:
			cur_index, value2 = arithmetic_fxn(symbol_table, cur_index)

		# typecasting the values to something that can be computed
		if valid_flag:
			value1, value2 = typcasting_arithmetic(value1, value2)

		# compares the two values and returns the lower value
		if valid_flag:
			if value1 < value2:
				return cur_index, value1
			else:
				return cur_index, value2
		else:
			return cur_index, None

def expressions(symbol_table, cur_index):
	# if the expression is an arithmetic one
	if symbol_table[cur_index][1] in arithmetic:
		cur_index,value = arithmetic_fxn(symbol_table, cur_index)
		return cur_index, value

	# if the expression is a boolean one
	elif symbol_table[cur_index][1] in boolean:
		cur_index,value = boolean_fxn(symbol_table, cur_index)
		return cur_index, value

	# if the expression is an infinite arity boolean one
	elif symbol_table[cur_index][1] in inf_bool:
		cur_index, value = inf_bool_fxn(symbol_table, cur_index)
		return cur_index, value

	# if the expression is a comparison one
	elif symbol_table[cur_index][1] in comparison:
		cur_index, value = comparison_fxn(symbol_table, cur_index)
		return cur_index, value

	# if the expression is an concatenation one
	elif symbol_table[cur_index][1] == "Concatenation":
		cur_index += 1
		cur_index, value = concatenation(symbol_table,cur_index)
		return cur_index, value

def assignment(symbol_table, cur_index, identifier):

	# if the assignment is done with a literal 
	if symbol_table[cur_index][1] in literals:
		value = symbol_table[cur_index][0]
		ent_type = check_type(value) 
		put_value(identifier, value, ent_type)
		cur_index += 1
		return cur_index

	# if the assignment is done with an identifier
	elif symbol_table[cur_index][1] == "Identifier":
		value = get_value(symbol_table[cur_index][0])
		ent_type = check_type(value) 
		put_value(identifier, value, ent_type)
		cur_index += 1
		return cur_index
	
	# if the assignment is done with an expression
	elif symbol_table[cur_index][1] in operations:
		cur_index, value = expressions(symbol_table, cur_index)
		ent_type = check_type(value) 
		put_value(identifier, value, ent_type)
		return cur_index

	# if a reassignment is being done
	elif symbol_table[cur_index][1] == "Typecasting_MAEK":
		cur_index += 1
		cur_index, value = explicit_typecasting(symbol_table, cur_index)
		ent_type = check_type(value)
		put_value(identifier, value, ent_type)
		return cur_index

def put_value(identifier, value, ent_type):
	global valid_flag
	nonexistent_flag = True
	# locates the variable identifier and stores the values to it
	for i in range(len(new_table)):
		if identifier == new_table[i][0]:
			new_table[i][1] = value
			new_table[i][2] = ent_type
			nonexistent_flag = False
	# prompts an error if the variable does not exist
	if nonexistent_flag:
		console.insert(tk.END, "Semantic Error: Assigning value to undeclared variable '" + identifier + "'")
		
		valid_flag = False

def submit(pop_up_entry, pop_up_window, symbol_table, cur_index):
	# if the entry field is not empty then process the value 
	if pop_up_entry.get():
		identifier = symbol_table[cur_index][0]
		value = pop_up_entry.get()
		pop_up_window.destroy()

		# insert the user input into the console window 
		string = ">>> " + value
		console.insert(tk.END, string)

		# stores it to the identifier specified
		# casted to "YARN" data type as specified in the documentation
		put_value(identifier, value, "YARN")
		cur_index += 1
		return cur_index

def inputing(symbol_table, cur_index):
	# creates a new pop up window
	pop_up_window = tk.Toplevel(main_window)
	pop_up_window.title("User Input")
	pop_up_window.columnconfigure(0, weight=1)

	# label to indicate what the user should do
	pop_up_label = tk.Label(pop_up_window, text= "Please enter user input:")
	pop_up_label.grid(row=0, column=0, padx=5, pady=5)
	
	# entry field for the user to put inputs in
	pop_up_entry = tk.Entry(pop_up_window, width=35)
	pop_up_entry.grid(row=1, column=0, padx=5, pady=5)

	# submit button
	pop_up_submit = tk.Button(pop_up_window, text="Submit", command=lambda : submit(pop_up_entry, pop_up_window, symbol_table, cur_index))
	pop_up_submit.grid(row=3, column=0, padx=5, pady=5)

	# waits for this window to be destroyed before returning
	pop_up_window.wait_window()
	return cur_index

def get_value(identifier):
	# gets the value of the identifier specified
	for i in range(len(new_table)):
		if identifier == new_table[i][0]:
			return new_table[i][1]
	# prompts an error if the identifier is not found
	console.insert(tk.END, "Semantic Error: Identifier '" + identifier + "' is not defined.")

	global valid_flag
	valid_flag = False
	
	return

def printing(symbol_table, cur_index):
	line_num = symbol_table[cur_index][2]

	# prints all the expressions as long as they are on the same line
	string = ''
	while valid_flag and symbol_table[cur_index][2] == line_num:
		if symbol_table[cur_index][1] in literals:
			string = string + str(symbol_table[cur_index][0])
			cur_index += 1
		
		elif symbol_table[cur_index][1] == "Identifier":
			value = get_value(symbol_table[cur_index][0])
			string = string + str(value)
			cur_index += 1

		elif symbol_table[cur_index][1] in operations:
			cur_index, value = expressions(symbol_table, cur_index)
			string = string + str(value)
	
	if valid_flag:
		console.insert(tk.END, string)
	
	return cur_index

def check_type(ent_val):
	# checks the data type given a value 
	if type(ent_val) == int:
		return "NUMBR"
	elif type(ent_val) == float:
		return "NUMBAR"
	elif ent_val == "WIN" or ent_val == "FAIL":
		return "TROOF"
	else:
		return "YARN"

def check_name(ent_name):
	# checks for the name of the variable in the new symbol table
	for i in range(len(new_table)):
		# if found return True and its index
		if ent_name == new_table[i][0]:
			return True, i
	# else return False and -1
	return False, -1
			
def declare(symbol_table, cur_index):
	# initial values for the symbol table entry
	ent_val = "NOOB"
	ent_type = "NOOB"
	ent_name = symbol_table[cur_index][0]

	# checks if the variable already exists and sets the flag appropriately
	existing_flag, existing_index = check_name(ent_name)

	cur_index += 1

	# if the value of the variable is initialized, obtain the value and its data type
	if symbol_table[cur_index][1] == "Variable Initialization":
		cur_index += 1
		if symbol_table[cur_index][1] in literals:
			ent_val = symbol_table[cur_index][0]
			ent_type = check_type(ent_val)
			cur_index += 1
		elif symbol_table[cur_index][1] == "Identifier":
			ent_val = get_value(symbol_table[cur_index][0])
			ent_type = check_type(ent_val)
			cur_index += 1
		elif symbol_table[cur_index][1] in operations:
			cur_index, ent_val = expressions(symbol_table, cur_index)
			ent_type = check_type(ent_val)

	entry = [ent_name, ent_val, ent_type]

	# if the variable already exists, update its entry
	if existing_flag:
		new_table[existing_index] = entry
	# else append a new entry
	else:
		new_table.append(entry)
	return cur_index

def code_block(symbol_table, cur_index):

	if symbol_table[cur_index][1] == "Variable Declaration":
		cur_index += 1
		cur_index = declare(symbol_table, cur_index)
		return cur_index

	elif symbol_table[cur_index][1] == "Output Keyword":
		cur_index += 1
		cur_index = printing(symbol_table, cur_index)
		return cur_index

	elif symbol_table[cur_index][1] == "Input Keyword":
		cur_index += 1
		cur_index = inputing(symbol_table, cur_index)
		return cur_index

	elif symbol_table[cur_index][1] == "Identifier":
		identifier = symbol_table[cur_index][0]
		cur_index += 1
		if symbol_table[cur_index][1] == "Variable Assignment":
			cur_index += 1
			cur_index = assignment(symbol_table, cur_index, identifier)
		elif symbol_table[cur_index][1] == "Typecasting_IS_NOW_A":
			cur_index += 1
			cur_index = recasting(symbol_table, cur_index, identifier)
		else:
			value = get_value(identifier)
			ent_type = check_type(value)
			new_table[0] = ["IT", value, ent_type]
		return cur_index

	elif symbol_table[cur_index][1] in literals:
		value = symbol_table[cur_index][0]
		ent_type = check_type(value)
		new_table[0] = ["IT", value, ent_type]
		cur_index += 1
		return cur_index

	elif symbol_table[cur_index][1] in operations:
		cur_index, value = expressions(symbol_table, cur_index)
		ent_type = check_type(value)
		new_table[0] = ["IT", value, ent_type]
		return cur_index

	elif symbol_table[cur_index][1] == "Typecasting_MAEK":
		cur_index += 1
		cur_index, value = explicit_typecasting(symbol_table, cur_index)
		ent_type = check_type(value)
		new_table[0] = ["IT", value, ent_type]
		return cur_index

	elif symbol_table[cur_index][1] == "If-Then Delimiter Start":
		cur_index += 1
		cur_index = if_then(symbol_table, cur_index)
		return cur_index

	elif symbol_table[cur_index][1] == "Switch-Case Delimiter Start":
		cur_index += 1
		cur_index = switch_case(symbol_table, cur_index)
		return cur_index

	elif symbol_table[cur_index][1] == "Loop Delimiter Start":
		cur_index += 1
		cur_index = looping(symbol_table, cur_index)
		return cur_index

	# else the word does not need to be assessed
	else:
		cur_index += 1
		return cur_index

def semantic(window, symbol_table, console_window):

	# makes the console window global for printing and inputing
	global console
	console = console_window

	# makes the main window global for printing and inputing
	global main_window
	main_window = window
	
	# initializes the updated symbol table which will contain all the details for each variable
	global new_table
	new_table = []

	# initializes the stack that will keep track of the loop identifiers
	global loop_stack
	loop_stack = []

	global valid_flag
	valid_flag = True

	# initializes the implicit variable IT and appends it to the new symbol table
	entry = ["IT", "NOOB", "NOOB"]
	new_table.append(entry)

	cur_index = 0
	# loops through the whole list
	while valid_flag and (cur_index < len(symbol_table)):
		# if the end of the code is reached, stop looping
		if symbol_table[cur_index][1] == "Code Delimiter End":
			break
		# else assess the code block
		else:
			cur_index = code_block(symbol_table, cur_index)

	# returns the final updated table
	return new_table, valid_flag