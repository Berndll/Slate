from assembler import assemble
from schematic import make_schematic

def main():
    program = 'collatz'

    as_filename = f'programs/{program}.as'
    mc_filename = f'programs/{program}.mc'
    schem_filename = f'{program}'

    assemble(as_filename, mc_filename)
    make_schematic(mc_filename, schem_filename)

if __name__ == '__main__':
    main()