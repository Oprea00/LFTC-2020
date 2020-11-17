from domain.Grammar import Grammar


def print_command_grammar():
    print("1 -> Set of non-terminals")
    print("2 -> Set of terminals")
    print("3 -> Set of productions of a non-terminal")
    print("4 -> Productions of a given terminal")
    print("5 -> Check if regular")
    print("0 -> Exit")


grammar = Grammar.read_from_file('g1.txt')
cmd = -1
while cmd != 0:
    print_command_grammar()
    cmd = int(input("Command: "))
    if cmd == 1:
        print("The set of non-terminals (N): ", grammar.N)
    elif cmd == 2:
        print("The set of terminals (E): ", grammar.E)
    elif cmd == 3:
        print("The set of productions (P): ", grammar.P)
    elif cmd == 4:
        symbol = input("The symbol: ")
        print(grammar.get_productions(symbol))
    elif cmd == 5:
        print(grammar.check_regular())
    else:
        break
