# !! --------- 
# Handle sys.exit() better

import sys
import lex
import syn
import sem
from copy import deepcopy

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk

def open_file(text_editor):
	file_path = askopenfilename(
		filetypes = [("Lolcode Files", "*.lol")]
	)

	if not file_path:
		return
	text_editor.delete(1.0, tk.END)
	with open(file_path, "r") as input_file:
		text = input_file.read()
		text_editor.insert(tk.END, text)

def create_text_editor(window):
	text_editor_frame = tk.Frame(window)
	text_editor = tk.Text(text_editor_frame)
	open_button = tk.Button(text_editor_frame, text="Open File", command= lambda : open_file(text_editor))

	open_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
	text_editor.grid(row=1, column=0, sticky="nsew")

	text_editor_frame.rowconfigure(0, weight=1)
	text_editor_frame.columnconfigure(0, weight=1)
	text_editor_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

	return text_editor

def create_lexeme_table(window):
	lexeme_table = ttk.Treeview(window, columns=("Lexeme", "Classification"), show="headings")
	lexeme_table.heading("#1", text="Lexeme")
	lexeme_table.heading("#2", text="Classification")
	
	lexeme_table.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

	return lexeme_table

def create_symbol_table(window):
	symbol_table = ttk.Treeview(window, column=("Identifier", "Value"), show="headings")
	symbol_table.heading("#1", text="Identifier")
	symbol_table.heading("#2", text="Value")
	
	symbol_table.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

	return symbol_table

def clear_fields(lexeme_table, symbol_table, console_window):

	console_window.delete(0, tk.END)

	for entry in lexeme_table.get_children():
		lexeme_table.delete(entry)

	for entry in symbol_table.get_children():
		symbol_table.delete(entry)

def interpret(window, text_editor, lexeme_table, symbol_table, console_window):

	clear_fields(lexeme_table, symbol_table, console_window)

	file_input = text_editor.get("1.0", "end-1c").splitlines()

	# LEXICAL ANALYSIS ======================================================================================
	
	# initializing the lexeme table
	lexical_table_entries = []
	# will contain all the multi comment lines
	multi_comment = []
	# indicates whether the line is a comment or not
	comment_flag = 0
	# indicates the line number which will be printed for lexical error prompt
	line_num = 1
	for line in file_input:

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
				lexical_table_entries.append(entry)
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
							lexical_table_entries.append(entry)
						# append the keyword to the symbol table
						entry = [word,  "Multiple Line Comment End", line_num]
						lexical_table_entries.append(entry)
						# update the flags
						tldr_flag = False
						comment_flag = 0
					# put the words into the comment string if not a keyword
					else:
						comment = comment + " " + word

				# if the TLDR keyword is not encountered, append the comment to the symbol table
				if tldr_flag:
					entry = [comment, "Comment Content", line_num]
					lexical_table_entries.append(entry)
		line_num += 1

	# SYNTAX ANALYSIS =======================================================================================

	# initiates a new symbol table that will disregard comments  
	lexeme_table_no_comments = []
	for i in range(len(lexical_table_entries)):
		# disregards OBTW keywords
		if lexical_table_entries[i][1] == "Multiple Line Comment Start":
			continue
		# disregards TLDR keywords
		elif lexical_table_entries[i][1] == "Multiple Line Comment End":
			continue
		# disregards BTW keywords
		elif lexical_table_entries[i][1] == "Single Line Comment":
			continue
		# disregards comment contents
		elif lexical_table_entries[i][1] == "Comment Content":
			continue
		# appends everything else
		else:
			lexeme_table_no_comments.append(lexical_table_entries[i])

	# checks the syntax of the code
	syntax_flag = False 
	syntax_flag = syn.syntax(lexeme_table_no_comments, console_window)

	# SEMANTIC ANALYSIS =====================================================================================
	semantic_flag = False

	# conducts semantic analysis on the code
	if syntax_flag:
		final_symbol_table, semantic_flag = sem.semantic(window, lexeme_table_no_comments, console_window)
		lexeme_table_no_comments.clear()

	if semantic_flag:
		# inserting the values of the lexeme table in the GUI
		for i in range(len(lexical_table_entries)):
			lexeme_table.insert("", tk.END, values=(lexical_table_entries[i][0], lexical_table_entries[i][1]))

		# inserting the values of the symbol table in the GUI
		for i in range(len(final_symbol_table)):
			symbol_table.insert("", tk.END, values=(final_symbol_table[i][0], final_symbol_table[i][1]))

def create_execute_button(window):
	execute_button = tk.Button(window, text="Execute", command=lambda : interpret(window, text_editor, lexeme_table, symbol_table, console_window))
	execute_button.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

	return execute_button

def create_console_window(window):
	console_window = tk.Listbox(window)
	console_window.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

	return console_window

window = tk.Tk()
window.state("zoomed")
window.title("Lolcode Interpreter")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

text_editor = create_text_editor(window)
lexeme_table = create_lexeme_table(window)
symbol_table = create_symbol_table(window)
execute_button = create_execute_button(window)
console_window = create_console_window(window)

window.mainloop()