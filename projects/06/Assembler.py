import sys
import os.path

labels = {'SP':0,
		  'LCL':1,
		  'ARG':2,
		  'THIS':3,
		  'THAT':4,
		  'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8,
		  'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
		  'SCREEN': 16384,
		  'KBD': 24576}

get_bin = lambda x, n: format(x, 'b').zfill(n) #get_bin(value, numdigits)

def dest_get(input):
	output = list('000')
	if input.find('A') <> -1:
		output[0] = '1'
	if input.find('D') <> -1:
		output[1] = '1'
	if input.find('M') <> -1:
		output[2] = '1'
	return "".join(output)

def jump_get(input):
	if input == 'JGT':
		output = '001'
	elif input == 'JEQ':
		output = '010'
	elif input == 'JGE':
		output = '011'
	elif input == 'JLT':
		output = '100'
	elif input == 'JNE':
		output = '101'
	elif input == 'JLE':
		output = '110'
	elif input == 'JMP':
		output = '111'
	else:
		output = '000'
	return output
	
def comp_get(input):
	if input.find('M') <> -1:
		output_A = '1'
		input = input.replace('M','A')
	else:
		output_A = '0'
	if input == '0':
		output = '101010'
	elif input == '1':
		output = '111111'
	elif input == '-1':
		output = '111010'
	elif input == 'D':
		output = '001100'
	elif input == 'A':
		output = '110000'
	elif input == '!D':
		output = '001101'
	elif input == '!A':
		output = '110001'
	elif input == '-D':
		output = '001111'
	elif input == '-A':
		output = '110011'
	elif input == 'D+1':
		output = '011111'
	elif input == 'A+1':
		output = '110111'
	elif input == 'D-1':
		output = '001110'
	elif input == 'A-1':
		output = '110010'
	elif input == 'D+A' or input == 'A+D':
		output = '000010'
	elif input == 'D-A':
		output = '010011'
	elif input == 'A-D':
		output = '000111'
	elif input.find('&') <> -1:
		output = '000000'
	elif input.find('|') <> -1:
		output = '010101'
	else:
		print 'Error finding comp for %s'%input
		output = 'ERROR'
	return output_A+output



if not len(sys.argv) == 2:
	print "Invalid arguments"
	quit()

readfile_path = os.path.join(os.getcwd(), sys.argv[1])
readfile = open(readfile_path, "r")
filename = os.path.splitext(readfile_path)[0]
writefile = open(filename+'.hack','w')

#Go through code, removing comments and whitespace, and adding (Xxxx) to symbol lookup
asmline_processed = []
for asmline_raw in readfile:
	asmline = ''.join(asmline_raw.split()) #Remove whitespace
	asmline = asmline.split('//')[0] #Remove comments
	if not asmline: #Line just comments and/or whitespace. Move on
		continue
	elif asmline[0] == '(': #Line is a label. Add to label directory and move on
		label = asmline.split('(')[1].split(')')[0]
		labels[label] = len(asmline_processed) #Sets to current line of code
		continue
	else:
		asmline_processed.append(asmline) #Add as line of code

openAddress = 16
		
for asmline in asmline_processed:
	if asmline[0] == '@':
		#A instruction
		if asmline[1].isdigit():
			address = int(asmline[1:])
		else:
			if asmline[1:] not in labels.keys():
				labels[asmline[1:]] = openAddress
				openAddress+=1
			address = labels[asmline[1:]]
					
		bin_line = get_bin(address, 16)
	
	else: 
		#C instruction
		bin_line = '111'
		tempstr = asmline
		dest_str = ''
		jump_str = ''
		if tempstr.find('=') <> -1: #Dest exists
			dest_str = tempstr.split('=')[0]
			tempstr = tempstr.split('=')[1]
		if tempstr.find(';') <> -1: #Jump exists
			jump_str = tempstr.split(';')[1]
		comp_str = tempstr.split(';')[0]
		
		print "Sep %s into Comp:%s Dest:%s Jump:%s"%(asmline,comp_str,dest_str,jump_str)
		
		dest_bin = dest_get(dest_str)
		comp_bin = comp_get(comp_str)
		jump_bin = jump_get(jump_str)
		
		print "Output: %s %s %s"%(comp_bin,dest_bin,jump_bin)
		
		bin_line = bin_line+comp_bin+dest_bin+jump_bin
			
	writefile.write(bin_line+'\n')
writefile.close()