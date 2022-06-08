'''
====================================== LOLCODE INTERPRETER ======================================

>>> AUTHOR				:	CABALDA, Elroy Christian D.

>>>	PROGRAM DESCRIPTION :	A program that takes a lolcode file (filename.lol) and performs
							lexical, syntax, and semantic analysis. This program will also run
							the lolcode file. Additionally, this program will display the symbol
							table that was used by the inputted lolcode file. 

>>> FILE DESCRIPTION	: 	This file performs lexical analysis on the lolcode file provided. 
	(lex.py)
'''

import sys 
import re

# gets one line of the input file and classifies each lexeme found in the line
def lexer(line, line_num):
	table = []
	lexeme_list = line.split() 			# word from file is a lexeme
	cur_index = 0						# current in the lexemes list
	lexeme = ''							# current lexeme
			
	while(cur_index < len(lexeme_list)):
		
		lexeme = lexeme_list[cur_index]

		# file opening and ending
		if (re.search(r"\bHAI\b",lexeme)):
			entry = [lexeme, "Code Delimiter Start", line_num]
		elif (re.search(r"\bKTHXBYE\b",lexeme)):
			entry = [lexeme, "Code Delimiter End", line_num]

		# comments
		elif (re.search(r"\bBTW\b", lexeme)):
			entry = [lexeme, "Single Line Comment", line_num]

			table.append(entry)

			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme_list[cur_index]

				while (cur_index < len(lexeme_list)):
					cur_index += 1
					if cur_index < len(lexeme_list):
						lexeme = lexeme + " " + lexeme_list[cur_index]

				entry = [lexeme, "Comment Content", line_num]
			else:
				entry = ["", "Comment Content", line_num]

		elif (re.search(r"\bOBTW\b",lexeme)):
			entry = [lexeme, "Multiple Line Comment Start", line_num]

			
			cur_index += 1
			if cur_index < len(lexeme_list):
				
				table.append(entry)
				comment = ""
				tldr_flag = False

				while (cur_index < len(lexeme_list)):
					lexeme = lexeme_list[cur_index]
					if (re.search(r"\bTLDR\b",lexeme)):
						entry = [comment, "Comment Content", line_num]
						table.append(entry)
						tldr_flag = True
					else:
						comment = comment + " " + lexeme
					cur_index += 1
				
				if tldr_flag:
					entry = [lexeme, "Multiple Line Comment End", line_num]
				else:
					entry = [comment, "Comment Content", line_num]

		# variable declaration
		elif (re.search(r"\bI\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bI HAS\b",lexeme)):
				cur_index += 1
				if cur_index < len(lexeme_list):
					lexeme = lexeme + " " + lexeme_list[cur_index]
				
				if (re.search(r"\bI HAS A\b",lexeme)):
					entry = [lexeme, "Variable Declaration", line_num]
				else:
					entry = [lexeme, "unknown_token", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "Identifier", line_num]
		elif (re.search(r"\bITZ\b",lexeme)):
			entry = [lexeme, "Variable Initialization", line_num]
		elif (re.search(r"\bR\b",lexeme)):
			entry = [lexeme, "Variable Assignment", line_num]

		# arithmetic operations
		elif (re.search(r"\bSUM\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bSUM OF\b",lexeme)):
				entry = [lexeme, "Addition", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "Identifier", line_num]

		elif (re.search(r"\bDIFF\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bDIFF OF\b",lexeme)):
				entry = [lexeme, "Subtraction", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "Identifier", line_num]
		elif (re.search(r"\bPRODUKT\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bPRODUKT OF\b",lexeme)):
				entry = [lexeme, "Multiplication", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "Identifier", line_num]
		elif (re.search(r"\bQUOSHUNT\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bQUOSHUNT OF\b",lexeme)):
				entry = [lexeme, "Division", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "Identifier", line_num]
		elif (re.search(r"\bMOD\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bMOD OF\b",lexeme)):
				entry = [lexeme, "Modulo", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "Identifier", line_num]
		elif (re.search(r"\bBIGGR\b",lexeme)):
			
			old_lexeme = lexeme
			old_index = cur_index

			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bBIGGR OF\b",lexeme)):
				entry = [lexeme, "Maximum", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bSMALLR\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bSMALLR OF\b",lexeme)):
				entry = [lexeme, "Minimum", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]

		# boolean operations
		elif (re.search(r"\bEITHER\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bEITHER OF\b",lexeme)):
				entry = [lexeme, "Or", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bWON\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bWON OF\b",lexeme)):
				entry = [lexeme, "Xor", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bNOT\b",lexeme)):
			entry = [lexeme, "Not", line_num]
		elif (re.search(r"\bALL\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bALL OF\b",lexeme)):
				entry = [lexeme, "Infinite And", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bANY\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bANY OF\b",lexeme)):
				entry = [lexeme, "Infinite Or", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bMKAY\b",lexeme)):
			entry = [lexeme, "Infinite Delimiter", line_num]
		elif (re.search(r"\bBOTH\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bBOTH OF\b",lexeme)):
				entry = [lexeme, "And", line_num]

		# comparison operations
			elif (re.search(r"\bBOTH SAEM\b",lexeme)):
				entry = [lexeme, "Equal", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]

		elif (re.search(r"\bDIFFRINT\b",lexeme)):
			entry = [lexeme, "Not Equal", line_num]

		# concatenation
		elif (re.search(r"\bSMOOSH\b",lexeme)):
			entry = [lexeme, "Concatenation", line_num]

		# typecasting
		elif (re.search(r"\bMAEK\b",lexeme)):
			entry = [lexeme, "Typecasting_MAEK", line_num]
		elif (re.search(r"\bA\b",lexeme)):
			entry = [lexeme, "Typecasting Separator", line_num]
		elif (re.search(r"\bIS\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bIS NOW\b",lexeme)):
				
				cur_index += 1
				if cur_index < len(lexeme_list):
					lexeme = lexeme + " " + lexeme_list[cur_index]
			
				if (re.search(r"\bIS NOW A\b",lexeme)):
					entry = [lexeme, "Typecasting_IS_NOW_A", line_num]
				else:
					entry = [lexeme, "unknown_token", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]

		# i/o operations
		elif (re.search(r"\bVISIBLE\b",lexeme)):
			entry = [lexeme, "Output Keyword", line_num]
		elif (re.search(r"\bGIMMEH\b",lexeme)):
			entry = [lexeme, "Input Keyword", line_num]

		# if-then statements
		elif (re.search(r"\bO\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bO RLY\b\?",lexeme)):
				entry = [lexeme, "If-Then Delimiter Start", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bYA\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bYA RLY\b",lexeme)):
				entry = [lexeme, "If Block", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bMEBBE\b",lexeme)):
			entry = [lexeme, "Else If Block", line_num]
		elif (re.search(r"\bNO\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bNO WAI\b",lexeme)):
				entry = [lexeme, "Else Block", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]

		# switch-case statements
		elif (re.search(r"\bWTF\b\?",lexeme)):
			entry = [lexeme, "Switch-Case Delimiter Start", line_num]
		elif (re.search(r"\bOMG\b",lexeme)):
			entry = [lexeme, "Case Block", line_num]
		elif (re.search(r"\bOMGWTF\b",lexeme)):
			entry = [lexeme, "Default Block", line_num]
		elif (re.search(r"\bGTFO\b",lexeme)):
			entry = [lexeme, "Switch-Case Block Break", line_num]

		# control flow delimiter
		elif (re.search(r"\bOIC\b",lexeme)):
			entry = [lexeme, "Control Flow Delimiter End", line_num]

		# loops
		elif (re.search(r"\bIM\b",lexeme)):

			old_lexeme = lexeme
			old_index = cur_index
			
			cur_index += 1
			if cur_index < len(lexeme_list):
				lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\bIM IN\b",lexeme)):
				
				cur_index += 1
				if cur_index < len(lexeme_list):
					lexeme = lexeme + " " + lexeme_list[cur_index]
				
				if (re.search(r"\bIM IN YR\b",lexeme)):
					entry = [lexeme, "Loop Delimiter Start", line_num]
				else:
					entry = [lexeme, "unknown_token", line_num]
			elif (re.search(r"\bIM OUTTA\b",lexeme)):
				
				cur_index += 1
				if cur_index < len(lexeme_list):
					lexeme = lexeme + " " + lexeme_list[cur_index]
				
				if (re.search(r"\bIM OUTTA YR\b",lexeme)):
					entry = [lexeme, "Loop Delimiter End", line_num]
				else:
					entry = [lexeme, "unknown_token", line_num]
			else:
				cur_index = old_index
				entry = [old_lexeme, "unknown_token", line_num]
		elif (re.search(r"\bUPPIN\b",lexeme)):
			entry = [lexeme, "Increment", line_num]
		elif (re.search(r"\bNERFIN\b",lexeme)):
			entry = [lexeme, "Decrement", line_num]
		elif (re.search(r"\bYR\b",lexeme)):
			entry = [lexeme, "Loop Reference", line_num]
		elif (re.search(r"\bTIL\b",lexeme)):
			entry = [lexeme, "Until", line_num]
		elif (re.search(r"\bWILE\b",lexeme)):
			entry = [lexeme, "While", line_num]

		# variable separator
		elif (re.search(r"\bAN\b",lexeme)):
			entry = [lexeme, "Variable Separator", line_num]

		# literals
		elif (re.search(r"\".*",lexeme)):
			
			if (re.search(r"\".*\"",lexeme)):
				str_content = False
			else:
				str_content = True

			while str_content:
				cur_index += 1
				if cur_index == len(lexeme_list):
					entry = [lexeme, "unknown_token", line_num]
					str_content = False

				elif (re.search(r".*\"",lexeme_list[cur_index])):
					lexeme = lexeme + " " + lexeme_list[cur_index]
					str_content = False
				else:
					lexeme = lexeme + " " + lexeme_list[cur_index]
			
			if (re.search(r"\".*\"",lexeme)):
				entry = [lexeme.strip('"'), "String Literal", line_num]
			else:
				entry = [lexeme, "unknown_token", line_num]
		elif (re.search(r"-?\b\d+\.\d+\b",lexeme)):
			entry = [float(lexeme), "Float Literal", line_num]
		elif (re.search(r"-?\b\d+\b",lexeme)):
			entry = [int(lexeme), "Integer Literal", line_num]
		elif (re.search(r"\bWIN\b",lexeme)):
			entry = [lexeme, "True", line_num]
		elif (re.search(r"\bFAIL\b",lexeme)):
			entry = [lexeme, "False", line_num]

		# data type
		elif (re.search(r"\bTROOF\b",lexeme)):
			entry = [lexeme, "Boolean Type", line_num]
		elif (re.search(r"\bNOOB\b",lexeme)):
			entry = [lexeme, "Null Type", line_num]
		elif (re.search(r"\bNUMBR\b",lexeme)):
			entry = [lexeme, "Integer Type", line_num]
		elif (re.search(r"\bNUMBAR\b",lexeme)):
			entry = [lexeme, "Float Type", line_num]
		elif (re.search(r"\bYARN\b",lexeme)):
			entry = [lexeme, "String Type", line_num]

		# identifiers
		elif (re.search(r"\b[a-zA-Z]\w*\b",lexeme)):
			entry = [lexeme, "Identifier", line_num]

		# invalid lexemes
		else:
			entry = [lexeme, "unknown_token", line_num]

		# prompts the user for a lexical error and exits the program
		if entry[1] == "unknown_token":
			print("Lexical Error: Unknown token '" + entry[0] + "' in line " + str(line_num))
			sys.exit()

		table.append(entry)
		cur_index += 1

	return table