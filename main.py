'''
====================================== LOLCODE INTERPRETER ======================================

>>> AUTHOR				:	CABALDA, Elroy Christian D.

>>>	PROGRAM DESCRIPTION :	A program that takes a lolcode file (filename.lol) and performs
							lexical, syntax, and semantic analysis. This program will also run
							the lolcode file. Additionally, this program will display the symbol
							table that was used by the inputted lolcode file. 

>>> FILE DESCRIPTION	: 	This file serves as the main file where all results are consolidated.
	(main.py) 

>>> PROGRESS HISTORY	:

		25.11.2021 - lexical analysis done
		30.11.2021 - lexical analysis overhaul
		02.12.2021 - syntax analysis (variable declaration, printing)
		07.12.2021 - syntax analysis (single comment, multiple comment, input, assignment)
		14.12.2021 - syntax analysis (loops, if-then, switch-case)
		27.12.2021 - syntax analysis (expressions)
		28.12.2021 - syntax analysis (comparison, concatenation, typecasting)
		29.12.2021 - lexical analysis tweaking (comment implementation)
					 syntax analysis tweaking 
		01.01.2022 - semantic analysis (declaration, printing, assignment, arithmetic, boolean, 
					 inf boolean)
		02.01.2022 - semantic analysis (comparison, concatenation, explicit typecasting, 
					 recasting if-then)
					 syntax analysis tweaking
		03.01.2022 - semantic analysis (switch case, loops)
					 semantic analysis tweaking
		10.01.2022 - gui (basic layout, input and textbox)
		11.01.2022 - gui (lexeme table, integrating lexical analysis and syntax analysis)
		12.01.2022 - gui (input and output handling by the console window)
		13.01.2022 - gui (tweaking ui and console window)
		14.01.2022 - gui (tweaking semantic analysis to handle errors better)
		17.01.2022 - semantic analysis tweaking (handling errors better)
					 lexical analysis tweaking (handling identifiers bettr)
					 syntax analysis tweaking (handling errors better)
		18.01.2022 - semantic analysis tweaking (error handling)
					 syntax analysis tweaking (error handling)
'''

import sys
import lex
import syn
import sem
from copy import deepcopy

# !! ======== CHANGE INPUT FILE HERE ======== !! 
f = open("input/sample.lol", "r")


# LEXICAL ANALYSIS ======================================================================================

# initializing the symbol table
symbol_table = []

# will contain all the multi comment lines
multi_comment = []
# indicates whether the line is a comment or not
comment_flag = 0
# indicates the line number which will be printed for lexical error prompt
line_num = 1
for line in f:

	# checks if the line contains a comment keyword
	line_split = line.split()
	if len(line_split) > 0:
		if line_split[0] == "BTW" or line_split[0] == "OBTW":
			comment_flag == 1

	# if the line is not a comment
	if comment_flag == 0:
		# get the type for each lexeme 
		lexical_output = lex.lexer(line, line_num)
		# for each lexeme append to the symbol table
		for entry in lexical_output:
			# if the lexeme is the start of a multi line comment
			if entry[1] == "Multiple Line Comment Start":
				# update the flag to indicate that the following lines are comments
				comment_flag = 1
			# if the lexeme is the end of a multi line comment on the same line
			elif entry[1] == "Multiple Line Comment End":
				# update the flag to indicate that the following lines are comments
				comment_flag = 0 
			symbol_table.append(entry)
	# if the line is a commment
	else:
		# split the line into words
		line_split = line.split()
		# indicates whether the TLDR keyword was encountered on the same line
		tldr_flag = True
		# will hold the comment content 
		comment = ""

		# if the line is not empty
		if len(line_split) > 0:
			# iterate through each word
			for word in line_split:
				# if the end keyword is encountered on the same line as the comments
				if word == "TLDR":
					# append the comment to the symbol table if it is not empty
					if comment != "":
						entry = [comment,  "Comment Content", line_num]
						symbol_table.append(entry)
					# append the keyword to the symbol table
					entry = [word,  "Multiple Line Comment End", line_num]
					symbol_table.append(entry)
					# update the flags
					tldr_flag = False
					comment_flag = 0
				# put the words into the comment string if not a keyword
				else:
					comment = comment + " " + word

			# if the TLDR keyword is not encountered, append the comment to the symbol table
			if tldr_flag:
				entry = [comment, "Comment Content", line_num]
				symbol_table.append(entry)
	line_num += 1

# prints the content of the symbol table
print("\nLEXEMES")
for lexeme in symbol_table:
	print("%20s \t%s" %(lexeme[0], lexeme[1]))

# SYNTAX ANALYSIS =======================================================================================

# initiates a new symbol table that will disregard comments  
symbol_table_no_comments = []
for i in range(len(symbol_table)):
	# disregards OBTW keywords
	if symbol_table[i][1] == "Multiple Line Comment Start":
		continue
	# disregards TLDR keywords
	elif symbol_table[i][1] == "Multiple Line Comment End":
		continue
	# disregards BTW keywords
	elif symbol_table[i][1] == "Single Line Comment":
		continue
	# disregards comment contents
	elif symbol_table[i][1] == "Comment Content":
		continue
	# appends everything else
	else:
		symbol_table_no_comments.append(symbol_table[i])

# checks the syntax of the code 
syn.syntax(symbol_table_no_comments)

# SEMANTIC ANALYSIS =====================================================================================

print("\nOUTPUT")
# conducts semantic analysis on the code
final_symbol_table = sem.semantic(symbol_table_no_comments)
symbol_table_no_comments.clear()

# prints out the updated symbol table
print("\nSYMBOL TABLE")
for entry in final_symbol_table:
	print(entry)