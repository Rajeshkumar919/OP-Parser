import sys
import shlex
import csv


def main():
	# testing of inputs
	input_string = open('input1.txt', 'r').readline()  # Correct Input
	# input_string = open('input2.txt', 'r').readline()  # Correct Input
	# input_string = open('input3.txt', 'r').readline()  # Two Operators togethor Input
	# input_string = open('input4.txt', 'r').readline()  # operator at end
	# input_string = open('input5.txt', 'r').readline()  # any other input not in grammer
	
	input_ind = list(shlex.shlex(input_string))
	input_ind.append('$')
	print()
	print("Input: ",input_string)
	print()
	print("Sybmol table for above input")
	sybmolTable={}
	# creating sybmol table
	c=0
	for i,val in enumerate(input_ind):
		if val in ['+','-','*','/']:
			sybmolTable[str(val)]="<"+val+">"
			c=c+1
		elif val in ['1','2','3','4','5','6','7','8','9']:
			sybmolTable[val]=val
		elif val not in ['$']:
			sybmolTable[str(val)]="<"+val+">"



	#printing Symbol Table
	print()
	print("      Symbol Table  ")
	print("______________________")
	print('{:12s}'.format("|   Lexem"),'{:8s}'.format("Token"),'{:8s}'.format("|"))
	print("______________________")
	for key,value in sybmolTable.items():
		print('{:10s}'.format("|    "+str(key)),'{:10s}'.format("|    "+str(value)),'{:10s}'.format("|"))
	print("______________________")



	# Reading Grammer from grammer.txt
	master = {}
	master_list = []
	new_list = []
	non_terminals = []
	grammar = open('grammar.txt', 'r')
	
	for row2 in grammar:
		
		if '->' in row2:
			if len(new_list) == 0:
				start_state = row2[0]
				non_terminals.append(row2[0])
				new_list = []
				new_list.append(row2.rstrip('\n'))
			else:
				master_list.append(new_list)
				del new_list
				new_list = []
				new_list.append(row2.rstrip('\n'))
				non_terminals.append(row2[0])
				
		
		elif '|' in row2:
			new_list.append(row2.rstrip('\n'))	
	

	master_list.append(new_list)
	
	
	for x in range(len(master_list)):
		for y in range(len(master_list[x])):
			master_list[x][y] = [s.replace('|', '') for s in master_list[x][y]]
			master_list[x][y] = ''.join(master_list[x][y])
			master[master_list[x][y]] = non_terminals[x] 

	for key, value in master.items():
		if '->' in key:
			length = len(key)
			for i in range(length):
				if key[i] == '-' and key[i + 1] == ">":
					index =  i+2
					break
			var_key = key
			new_key = key[index:]
	
	var = master[var_key]
	del master[var_key]
	master[new_key] = var	
	

	# reading parsing table from file.
	order_table = []
	with open('order.csv', 'r') as file2:
		order = csv.reader(file2)
		print()
		print("                              Parsing Table:")
		temp=0
		for i,row in enumerate(order):
			if(i==0):
				print("   ___",end="")
				for _ in range(len(row)):
					print("____",end="")        
				print()
				temp=len(row)
			print("   |",end="")
			order_table.append(row)                    
			for j,cell in enumerate(row):
				if i==0 and j==1:
					print("   "+cell+" ", end="")
				elif cell == " ":
					print("   "+" ", end="")
				else:
					print("  "+cell+" ", end="")

			print("  |")
		print("   ___",end="")
		for _ in range(0,temp):
			print("____",end="")        
		print()
		print()
		print()

	operators = order_table[0]
	# printing error message if occurs.
	for val in input_ind:
		if val not in operators:
			print("\n")
			print("****************************************************************************")
			print(" Rejected!! "+ val +" is not generated, Hence Violates Grammer Rules. ")
			print("****************************************************************************")
			return			


	# Here starts the whole parsing and steps are also shown
	# in output with awesome UI
	stack = []
	stack.append('$') 
	print()
	print("__________________________________________________________________________________________________________________________________________________________________")
	print("                                                                        Syntax Analysis")
	print("__________________________________________________________________________________________________________________________________________________________________")
	print('{:50s}'.format("   Stack"), '{:70s}'.format("Input"),'{:25s}'.format("Precedence relation") , '{:8s}'.format("Action"))
	
	error=""
	vlaag = 1
	while vlaag:
		
		if input_ind[0] == '$' and len(stack)==2:
			vlaag = 0
		elif input_ind[0] == '$' and (len(stack) == 3):
			vlaag = -1
		elif len(input_ind) == 2:
			if '+' in input_ind:
				vlaag = -1
			if '-' in input_ind:	
				vlaag = -1
			if '*' in input_ind:
				vlaag = -1
			if '/' in input_ind:
				vlaag = -1
			error = error + "Operator at the end of expression"

		length = len(input_ind)

		buffer_inp = input_ind[0] 

		if (buffer_inp in ['+','-','/','*'] and stack[len(stack)-1] in ['+','-','/','*']) or input_string[0] in ['+','-','/','*']	:
			vlaag=-1
			if input_string[0] in ['+','-','/','*']:
				error = error + "Operator at Start"
			else:
				error = error + "Two Operators together"

		temp1 = operators.index(str(buffer_inp))
		print("   stack",stack, stack[-1])
		if stack[-1] in non_terminals:
			buffer_stack = stack[-2]
		else:
			buffer_stack = stack[-1]
		temp2 = operators.index(str(buffer_stack))
					
		precedence = order_table[temp2][temp1]
			
		if precedence == '<':
			action = 'shift'
		elif precedence == '>':
			action = 'reduce'
		
		print('{:50s}'.format("   "+str(stack)), '{:70s}'.format(str(input_ind)), '{:25s}'.format("      "+precedence), '{:8s}'.format(action))		
		
		if action == 'shift':
			stack.append(buffer_inp)
			input_ind.remove(buffer_inp)
		elif action == 'reduce':
			for key, value in master.items():
				var1 = ''.join(stack[-1:])
				var2 = ''.join(stack[-3:])
				if str(key) == str(buffer_stack):
					stack[-1] = value
					break
				elif key == var1 or stack[-3:]==list(var1):
					stack[-3:] = value
					break
				elif key == var2:
					stack[-3:] = value	
		del buffer_inp, temp1, buffer_stack, temp2, precedence

		# final conditions which also does error checking
		if vlaag == 0:
			print("\n")
			print("**************************************")
			print("*               Accepted!            *")
			print("**************************************")
		elif vlaag == -1:
			print("\n")
			print("****************************************************************************")
			print(" Rejected!! "+error + ". Hence Violates Grammer Rules. ")
			print("****************************************************************************")
			return

	return
	
main()