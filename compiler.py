# MODIFIED VERSION OF https://github.com/mattbatwings/BatPU-2/blob/main/assembler.py!!!!!!

import sys
import os

def assemble(assembly_filename, mc_filename):
    assembly_file = open(assembly_filename, 'r')
    machine_code_file = open(mc_filename, 'w')
    lines = (line.strip() for line in assembly_file)
    ctr = 1

    # Remove comments and blanklines
    for comment_symbol in ['/', ';', '#']:
        lines = [line.split(comment_symbol)[0] for line in lines]
    lines = [line for line in lines if line.strip()]

    # Populate symbol table
    symbols = {}
    
    opcodes = ['nop', 'hlt', 'add', 'sub', 'and', 'or', 'xor', 'rsh', 'ldi', 'adi', 'jmp', 'brh', 'cal', 'ret', 'lod', 'str', 'pld', 'pst']
    for index, symbol in enumerate(opcodes):
        symbols[symbol] = index
    
    registers = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
    for index, symbol in enumerate(registers):
        symbols[symbol] = index

    conditions1 = ['eq', 'ne', 'ge', 'lt']
    conditions2 = ['=', '!=', '>=', '<']
    conditions3 = ['z', 'nz', 'c', 'nc']
    conditions4 = ['zero', 'notzero', 'carry', 'notcarry']
    for index, symbol in enumerate(conditions1):
        symbols[symbol] = index
    for index, symbol in enumerate(conditions2):
        symbols[symbol] = index
    for index, symbol in enumerate(conditions3):
        symbols[symbol] = index
    for index, symbol in enumerate(conditions4):
        symbols[symbol] = index

    # Extract definitions and labels
    def is_definition(word):
        return word == 'define'
    
    def is_label(word):
        return word[0] == '.'
    
    pc = 0
    instructions = []

    machine_code_file.write("v3.0 hex words addressed\n")
    
    for index, line in enumerate(lines):
        words = [word.lower() for word in line.split()]

        if is_definition(words[0]):
            symbols[words[1]] = int(words[2])
        elif is_label(words[0]):
            symbols[words[0]] = pc
            if len(words) > 1:
                pc += 1
                instructions.append(words[1:])
        else:
            pc += 1
            instructions.append(words)

    # Generate machine code
    def resolve(word):
        if word[0] in '-0123456789':
            return int(word, 0)
        if symbols.get(word) is None:
            exit(f'Could not resolve {word}')
        return symbols[word]

    for pc, words in enumerate(instructions):
        # Resolve pseudo-instructions
        if words[0] == 'cmp':
            words = ['sub', words[1], words[2], registers[0]] # sub A B r0
        elif words[0] == 'mov':
            words = ['add', words[1], registers[0], words[2], ] # add A r0 dest
        elif words[0] == 'lsh':
            words = ['add', words[1], words[1], words[2]] # add A A dest
        elif words[0] == 'inc':
            words = ['adi', words[1], '1'] # adi dest 1
        elif words[0] == 'dec':
            words = ['adi', words[1], '-1'] # adi dest -1
        elif words[0] == "neg":
            words = ["sub", registers[0], words[1], words[2]] # sub r0 A dest

        # lod/str optional offset
        if words[0] in ['lod', 'str', 'pld', 'pst'] and len(words) == 3:
            words.append('0')

        # space special case
        if words[-1] in ['"', "'"] and words[-2] in ['"', "'"]:
            words = words[:-1]
            words[-1] = "' '"
        
        # Begin translation
        opcode = words[0]
        machine_code = symbols[opcode] << 12
        words = [resolve(word) for word in words]

        # Number of operands check
        if opcode in ['nop', 'hlt', 'ret'] and len(words) != 1:
            exit(f'Incorrect number of operands for {opcode} on line {pc}')
        
        if opcode in ['jmp', 'cal'] and len(words) != 2:
            exit(f'Incorrect number of operands for {opcode} on line {pc}')

        if opcode in ['rsh', 'ldi', 'adi', 'brh'] and len(words) != 3:
            exit(f'Incorrect number of operands for {opcode} on line {pc}')

        if opcode in ['add', 'sub', 'and', 'or', 'xor', 'lod', 'str', 'pld', 'pst'] and len(words) != 4:
            exit(f'Incorrect number of operands for {opcode} on line {pc}')

        # Reg A
        if opcode in ['add', 'sub', 'and', 'or', 'xor', 'rsh', 'ldi', 'adi', 'lod', 'str', 'pld', 'pst']:
            if words[1] != (words[1] % (2 ** 4)):
                exit(f'Invalid reg A for {opcode} on line {pc}')
            machine_code |= (words[1] << 8)

        # Reg B
        if opcode in ['add', 'sub', 'and', 'or', 'xor', 'lod', 'str', 'pld', 'pst']:
            if words[2] != (words[2] % (2 ** 4)):
                exit(f'Invalid reg B for {opcode} on line {pc}')
            machine_code |= (words[2] << 4)

        # Reg C
        if opcode in ['add', 'sub', 'and', 'or', 'xor', 'rsh']:
            if words[-1] != (words[-1] % (2 ** 4)):
                exit(f'Invalid reg C for {opcode} on line {pc}')
            machine_code |= words[-1]

        # Immediate
        if opcode in ['ldi', 'adi']:
            if words[2] < -128 or words[2] > 255: # 2s comp [-128, 127] or uint [0, 255]
                exit(f'Invalid immediate for {opcode} on line {pc}')
            machine_code |= words[2] & (2 ** 8 - 1)
        
        # Instruction memory address
        if opcode in ['jmp', 'brh', 'cal']:
            if words[-1] != (words[-1] % (2 ** 10)):
                exit(f'Invalid instruction memory address for {opcode} on line {pc}')
            machine_code |= words[-1]

        # Condition
        if opcode in ['brh']:
            if words[1] != (words[1] % (2 ** 2)):
                exit(f'Invalid condition for {opcode} on line {pc}')
            machine_code |= (words[1] << 10)

        # Offset
        if opcode in ['lod', 'str', 'pld', 'pst']:
            if words[3] < -8 or words[3] > 7: # 2s comp [-8, 7]
                exit(f'Invalid offset for {opcode} on line {pc}')
            machine_code |= words[3] & (2 ** 4 - 1)

        as_string = hex(machine_code)[2:].rjust(5, '0')
        pc_string = hex(pc)[2:].rjust(3, '0')
        
        if(pc % 8 == 0) :
            machine_code_file.write(f'{pc_string} : ')

        machine_code_file.write(f'{as_string} ')
        
        if((pc+1)/8 == ctr) :
            machine_code_file.write("\n")
            ctr+=1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Not enough arguments.")


assemble(sys.argv[1], os.path.splitext(sys.argv[1])[0] + ".cmpl")
