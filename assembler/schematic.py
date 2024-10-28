import mcschematic

def make_schematic(mc_filename, schem_filename):
    schem = mcschematic.MCSchematic()

    hex_lines = [[int]]

    with open(mc_filename, 'r') as mc_file:
        lines = mc_file.readlines()
        reorder_lines(lines)

    hex_lines = merge_to_hex()

    x = 0
    z = 0
    for line in hex_lines:
        line.reverse()
        print(line)
        y = -1
        if x >= 32:
            z += 4
            x = 0
        for bit, ss in enumerate(line):
            if bit == 8:
                z += 2
                y = -1
            if ss == 0:
                schem.setBlock( (x, y, z), "minecraft:gray_concrete" )
            else:
                schem.setBlock( (x, y, z), mcschematic.BlockDataDB.BARREL.fromSS(ss) )
            y -= 2
        z -= 2
        x += 2

    schem.save("schems", schem_filename, mcschematic.Version.JE_1_20_1)

def reorder_lines(lines):
    temp_file = open("temp.mc", 'w')

    offset = 16
    output = []
    i = 0
    while i < len(lines):
        for count in range(4):
            idx = i + count * offset

            if idx < len(lines):
                output.append(lines[idx])
            else:
                output.append("0000000000000000\n")

            if (idx + 1) % (4 * offset) == 0:
                print("SAME")
                i = idx
        i += 1

    for line in output:
        temp_file.write(line)
    temp_file.close()

def merge_to_hex() -> list[list[int]]:
    temp_file = open("temp.mc", "r")
    lines = temp_file.readlines()
    temp_file.close()

    # Convert each line from binary string to integer
    as_bin = [int(line, base=2) for line in lines]

    # Initialize hex_output with separate lists for each line block
    hex_output = [[0] * 16 for _ in range(len(lines) // 4)]

    i = 0
    while i < len(as_bin):
        hex_line = [0] * 16
        for bit in range(16):
            hex_bit = 0
            for n in range(4):
                hex_bit |= ((as_bin[i + n] & (1 << bit)) >> bit) << n

            hex_line[bit] = hex_bit
        hex_output[i // 4] = hex_line  # Assign to a specific block in hex_output

        print(hex_line)  # For verification, should only print once per set of 16 values
        i += 4

    print("")  # Newline after hex output
    return hex_output
