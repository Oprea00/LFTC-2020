from domain.FiniteAutomata import FiniteAutomata


def print_command_fa():
    print("1 -> Set of states")
    print("2 -> Alphabet")
    print("3 -> Transitions")
    print("4 -> Final States")
    print("5 -> Verify if input is accepted by FA")
    print("0 -> Exit")


def main():
    print("Reading finite automata from file..")
    fa = FiniteAutomata.read_from_file('fa.txt')
    cmd = 5
    while cmd != 0:
        print_command_fa()
        # cmd = int(input("Give option:"))
        if cmd == 1:
            print("The set of states (Q):", fa.Q)
        elif cmd == 2:
            print("Alphabet:", fa.E)
        elif cmd == 3:
            print("The transitions (D):", fa.D)
        elif cmd == 4:
            print("The set of final states (F):", fa.F)
        elif cmd == 5:
            sequence = input("Input: ")
            if fa.is_accepted(sequence):
                print("Sequence is accepted.")
            else:
                print("Invalid Sequence.")
        print()
        cmd = 0


main()
