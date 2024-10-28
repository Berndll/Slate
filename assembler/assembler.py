import sys

def assemble(as_filename, mc_filename):
    # ass is assembly, mc is machine code
    ass_file = open(as_filename, 'r')
    mc_file = open(mc_filename, 'w')

    # Remove whitespaces per line and store in array
    lines = (line.strip() for line in ass_file)

    # Remove comments and blanklines
    for comment_symbol in ['/', ';', '#']:
        lines = [line.split(comment_symbol)[0] for line in lines]
    lines = [line for line in lines if line.strip()]

    # Populate symbol table
    symbols = {}

    opcodes = [
        'nop', 'hlt', 'add', 'adi', 'sub', 'inc', 'dec', 'and',
        'ior', 'xor', 'ror', 'rol', 'not', 'cmp', 'cpi', 'lia',
        'lir', 'rld', 'rst', 'pld', 'pst', 'mld', 'mst', 'psh',
        'pop', 'mlt', 'mli', 'brh', 'jrl', 'cal', 'ret'
    ]    
    for index, symbol in enumerate(opcodes):
        symbols[symbol] = index

    registers = [ 'r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7' ]
    for index, symbol in enumerate(registers):
        symbols[symbol] = index

    conditions1 = [ 'true', 'neg', 'eq', 'neq', 'gt', 'lt', 'geq', 'leq' ]
    conditions2 = [    '1',   '-',  '=',  '!=',  '>',  '<',  '>=',   '<' ]
    for index, symbol in enumerate(conditions1):
        symbols[symbol] = index
    for index, symbol in enumerate(conditions2):
        symbols[symbol] = index

    # ports = [...]
    # for index, symbol in enumerate(ports):
    #     symbols[symbol] = index

    for i, letter in enumerate([' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '!', '?']):
        symbols[f'"{letter}"'] = i

    # Extract definitions and labels
    def is_definition(word):
        return word == 'define'
    
    def is_label(word):
        return word[0] == '.'
    
    def is_two_cycle(word):
        return words[0] == 'brh' or words[0] == 'cal'
    
    pc = 0
    instructions = []

    for index, line in enumerate(lines):
        words = [word.lower() for word in line.split()]

        # Process and set definitions
        if is_definition(words[0]):
            symbols[words[1]] = int(words[2])

        # Process labels
        elif is_label(words[0]):
            symbols[words[0]] = pc
            # Makes e.g.: ".label ADD" possible
            if len(words) > 1:
                pc += 1
                instructions.append(words[1:])

        else:
            pc += 1
            instructions.append(words)

        # 2 cycle instructions
        if is_two_cycle(words[0]):
            lines.insert(index + 1, 'upa')

    # Generate machine code
    def resolve(word):
        if word[0] in '-0123456789':
            return int(word, 0)
        if symbols.get(word) is None:
            exit(f'Could not resolve {word}')
        return symbols[word]

    last_jmp_adr = 0

    for pc, words in enumerate(instructions):
        # Begin translation
        opcode = words[0]
        if opcode in opcodes:
            machine_code = symbols[opcode] << 11
            words = [resolve(word) for word in words]
        elif opcode == 'upa':
            machine_code = 0

        # Number of operands check
        if opcode in [ 'nop', 'hlt', 'inc', 'dec', 'ror', 'rol', 'not', 'psh', 'pop', 'ret', 'upa' ] and len(words) != 1:
            exit(f'Incorrect number of operands for {opcode} on line {pc}') # 0 operands

        if opcode in [
            'add', 'adi', 'sub', 'and', 'ior', 'xor', 'cmp', 'cpi',
            'lia', 'rld', 'rst', 'pld', 'pst', 'mld', 'mst', 'mlt',
            'mli', 'cal'
            ] and len(words) != 2:
            exit(f'Incorrect number of operands for {opcode} on line {pc}') # 1 operand

        if opcode in [ 'lir', 'brh', 'jrl'] and len(words) != 3:
            exit(f'Incorrect number of operands for {opcode} on line {pc}') # 2 operands

        # Reg
        if opcode in ['add', 'sub', 'and', 'ior', 'xor', 'cmp', 'lir', 'rld', 'rst', 'pld', 'pst', 'mld', 'mst', 'mlt', 'jrl']:
            if words[1] != words[1] % (2 ** 3): # 3 bits
                exit(f'Invalid reg for {opcode} on line {pc}')
            machine_code |= words[1] << 8
        
        # Immediates
        if opcode in ['adi', 'cpi', 'lia', 'mli']:
            if words[1] != words[1] % (2 ** 8): # 8 bits
                exit(f'Invalid immediate for {opcode} on line {pc}')
            machine_code |= words[1]

        # Immediates with regs
        if opcode in ['lir']:
            if words[2] != words[2] % (2 ** 8): # 8 bits
                exit(f'Invalid immediate for {opcode} on line {pc}')
            machine_code |= words[2]

        # Branch
        if opcode in ['brh']:
            if words[1] != words[1] % (2 ** 3): # 3 bits
                exit(f'Invalid condition for {opcode} on line {pc}')
            # if words[2] != words[2] % (2 ** 8): # 8 bits
            #     exit(f'Invalid memory address for {opcode} on line {pc}')
            machine_code |= (words[1] << 8) | (words[2] % (2 ** 8))
            last_jmp_adr = words[2]

        # Upper Address
        if opcode in ['upa']:
            machine_code |= last_jmp_adr >> 8



        # # Offset
        # if opcode in ['jrl']:
        #     if words[1] != words[1] % (2 ** 3): # 3 bits
        #         exit(f'Invalid memory address for {opcode} on line {pc}')
        #     machine_code |= words[1] << 8

        # Memory Address
        if opcode in ['cal']:
            if words[1] != words[1] % (2 ** 3): # 3 bits
                exit(f'Invalid memory address for {opcode} on line {pc}')
            machine_code |= words[1] << 8

        # Merge and write
        as_string = bin(machine_code)[2:].rjust(16, '0')
        mc_file.write(f'{as_string}\n')            

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("Not enough arguments.")

    assemble(sys.argv[1], sys.argv[2] if len(sys.argv) >= 3 else 'output.mc')