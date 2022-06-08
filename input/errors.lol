HAI 1.2

	BTW ERROR 1: Using uninitialized variables
	I HAS A var1 ITZ "Now valid"
	VISIBLE var1

	BTW ERROR 2: Not delimiting Infinite Arity Boolean Operation
	VISIBLE ALL OF WIN AN 1 AN 1.0 AN "string" MKAY

	BTW ERROR 3: Mismatch of loop identifiers
	I HAS A loopvar ITZ 1
	IM IN YR loop_ident UPPIN YR loopvar TIL BOTH SAEM loopvar AN 3
		VISIBLE "loopvar = " loopvar
	IM OUTTA YR not_loop_ident
	BTW IM OUTTA YR not_loop_ident

	BTW ERROR 4: Comparing non NUMBR or NUMBAR types
	VISIBLE "1 == 2" BOTH SAEM 1 AN 2
	BTW VISIBLE "WIN == FAIL" BOTH SAEM WIN AN FAIL

	BTW ERROR 5: Nesting of Infinite Arity Boolean Operations
	VISIBLE "Nesting Boolean : " ALL OF WIN AN WIN AN BOTH OF FAIL AN FAIL AN WIN MKAY
	BTW VISIBLE "Nesting Infinite Arity :" ALL OF WIN AN WIN AN ANY OF FAIL AN FAIL AN FAIL MKAY

BTW ERROR 6: Not closing delimiters
KTHXBYE