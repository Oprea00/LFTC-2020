class FiniteAutomata:
    def __init__(self, q, e, d, q0, f):
        self.Q = q
        self.E = e
        self.D = d
        self.q0 = q0
        self.F = f

    @staticmethod
    def parse_line(line):
        """
        Read elements between curly brackets and return them in lists.
        :param line:
        :return:
        """
        return [element.strip() for element in line.strip().split('=')[1].strip()[1:-1].split(',')]

    @staticmethod
    def read_transitions(text):
        """
        Read the transitions (D) of the FA from file.
        :param text: string from file between '{}'
        :return: list of tuples
        """
        result = []
        for rule in text:
            [lhs, rhs] = rule.strip().split('-')
            [i, j] = lhs.strip()[1:-1].split(' ')
            result.append(((i, j), rhs.strip()))
        return result

    @staticmethod
    def read_from_file(filename):
        """
        Read the FA from file and store it in an object.
        Q - list of characters
        A - list of characters
        D - list of tuples (('p', '0'), 'q')
        F - list of characters
        :param filename: Text file from which we read.
        :return: A new FiniteAutomata object storing multiple lists.
        """
        with open(filename) as file:
            Q = FiniteAutomata.parse_line(file.readline())
            E = FiniteAutomata.parse_line(file.readline())
            q0 = FiniteAutomata.parse_line(file.readline())
            F = FiniteAutomata.parse_line(file.readline())
            D = FiniteAutomata.read_transitions(FiniteAutomata.parse_line(''.join([line for line in file])))
        return FiniteAutomata(Q, E, D, q0, F)

    def check_alphabet(self, input_sequence):
        """
        Check if some string contains only characters from the FA alphabet.
        :param input_sequence: String of chars
        :return: True if ok, False otherwise
        """
        ok = [c for c in input_sequence if c in self.E]
        if len(ok) < len(input_sequence):
            return False
        return True

    def is_accepted(self, input_sequence):
        """
        Check if a sequence is accepted by the FA.
        :param input_sequence:
        :return:
        """
        if not self.check_alphabet(input_sequence):
            print("Alphabet of input sequence is wrong!")
            return False

        # Iterate transitions and check if we reach epsilon (empty word)
        current_state = self.q0[0]
        print(self.D)
        for current_char in input_sequence:
            found_transition = False
            # Check if we can transit
            for transition in self.D:
                if found_transition:
                    continue
                if current_state == transition[0][0] and current_char == transition[0][1]:
                    # Successfully found a transition from this state
                    current_state = transition[1]
                    found_transition = True
            # If no transition found
            if not found_transition:
                return False

        if current_state in self.F:
            return True

        return False
