class Parser:
    """
    The LR(0) parser algorithm.
    """

    def __init__(self, grammar):
        self.grammar = grammar
        self.workingStack = []
        self.inputStack = []
        self.output = []

    def closure(self, productions):
        """
        Constructs one clojure of the canonical collections.
        Takes a state containing productions.
        :param productions: List of productions for closure
        :return: a state. List of tuples
        [('S1', ['.', 'S']), ('S', ['.', 'aA']), ('S', ['.', 'bB'])],
        """
        if not productions:
            return None
        closure = productions
        done = False
        while not done:
            done = True
            # Iterate each production in the state/clojure
            for dotted_prod in closure:
                dot_index = dotted_prod[1].index('.')  # where is dot in rhs
                alpha = dotted_prod[1][:dot_index]  # what is left of the dot
                b_beta = dotted_prod[1][dot_index + 1:]  # what is right of the dot

                # If nothing after dot, then is final state
                if len(b_beta) == 0:
                    continue

                B = b_beta[0]
                if B in self.grammar.E:
                    continue
                for prod in self.grammar.get_productions(B):
                    # adds item formed from production with dot in front of rhs of the production
                    dotted_prod = (B, ['.'] + prod)
                    if dotted_prod not in closure:
                        closure += [dotted_prod]
                        done = False
        return closure

    def go_to(self, state, symbol):
        """
        Transition from a state to another using a terminal or non-terminal.
        Used in generating parsing table and the canonical collection.
        :param state: String
        :param symbol: String
        :return: a state, list of tuples
        """
        C = []
        # in state search for LR(0) item that has dot in front of symbol
        for production in state:
            dot_index = production[1].index('.')
            alpha = production[1][:dot_index]
            xbeta = production[1][dot_index + 1:]
            if len(xbeta) == 0:
                continue
            X, beta = xbeta[0], xbeta[1:]
            if X == symbol:
                # move the dot after the symbol
                res = alpha + [X] + ['.'] + beta
                result_prod = (production[0], res)
                C += [result_prod]
        # call closure on this new item
        return self.closure(C)

    def get_canonical_collection(self):
        """
        Constructs set of states.
        C - canonical collection
        ex: [
        [('S1', ['.', 'S']), ('S', ['.', 'aA']), ('S', ['.', 'bB'])],
        [('S1', ['S', '.'])],
        ...
        ]
        :return: Collection of states
        """
        C = [self.closure([('S1', ['.', self.grammar.S[0]])])]  # augment the grammar
        finished = False
        while not finished:  # while we add a new state to the collection
            finished = True
            for state in C:
                for symbol in self.grammar.N + self.grammar.E:
                    next_state = self.go_to(state, symbol)
                    if next_state is not None and next_state not in C:
                        C += [next_state]
                        finished = False
        return C

    def generate_table(self):
        """
        Generates the parsing table used to check the input tokens.
        A dictionary for each state I ~ the rows
        :return: parsing table. List of dictionaries containing action and maybe non/terminals
        [{'action': 'shift', 'S': 1, 'A': 2, 'a': 3, 'b': 4}, {'action': 'acc'},
        {'action': 'shift', 'A': 6, 'a': 3, 'b': 4}, {'action': 'reduce 2'}, {'action': 'reduce 1'}]
        """
        states = self.get_canonical_collection()
        self.print_canonical_collection(states)
        table = [{} for _ in range(len(states))]

        for index in range(len(states)):
            state = states[index]
            first_rule_cnt = 0
            second_rule_cnt = 0
            third_rule_cnt = 0
            beta = []
            for prod in state:
                dot_index = prod[1].index('.')
                alpha = prod[1][:dot_index]
                beta = prod[1][dot_index + 1:]
                if len(beta) != 0:
                    first_rule_cnt += 1
                else:
                    if prod[0] != 'S1':
                        second_rule_cnt += 1
                        production_index = self.grammar.P.index((prod[0], alpha))
                    elif alpha == [self.grammar.S[0]]:
                        third_rule_cnt += 1
            if first_rule_cnt == len(state):
                table[index]['action'] = 'shift'

            elif second_rule_cnt == len(state):
                table[index]['action'] = 'reduce ' + str(production_index)

            elif third_rule_cnt == len(state):
                table[index]['action'] = 'acc'
            else:
                conflict_msg = 'Conflict! State I' + str(index) + ': ' + str(state) + '\nSymbol: ' + beta[0]
                raise (Exception(conflict_msg))
            for symbol in self.grammar.N + self.grammar.E:  # the goto part of the table
                next_state = self.go_to(state, symbol)
                if next_state in states:
                    table[index][symbol] = states.index(next_state)
        # print(table)
        return table

    def parse(self, input_string):
        """
        inputStack - list of strings. PIF code for each token read from txt file.
            ['33', '18', '19', '16', '25', '0', '6', '1', '15', '31', '0', '15', '17']
        table - [{'action': 'shift', 'S': 1, 'A': 2, 'a': 3, 'b': 4}, {'action': 'acc'},
            {'action': 'shift', 'A': 5, 'a': 3, 'b': 4}, {'action': 'shift', 'A': 6, 'a': 3, 'b': 4},
            {'action': 'reduce 2'}, {'action': 'reduce 0'}, {'action': 'reduce 1'}]
        workingStack - used to parse the inputStack
            ['0']
        :param input_string: list of strings, equal to inputStack
        :return: output - [0,2,1,1,2]
        S -> .. -> aabb
        List of integers representing reduce states. Each production rule has a number/reduce_state).
        Output is the list of steps needed to obtain the input_string starting from starting non-terminal S.
        """
        table = self.generate_table()
        self.workingStack = ['0']
        self.inputStack = [char for char in input_string]
        self.output = []
        while len(self.workingStack) != 0:
            state = int(self.workingStack[-1])  # which dict from parsing table, index of state
            if len(self.inputStack) > 0:
                char = self.inputStack.pop(0)
            else:
                char = None
            if table[state]['action'] == 'shift':
                # Shift operation on the stack
                if char not in table[state]:
                    raise (Exception('Cannot parse shift. Character: ', char))
                self.workingStack.append(char)
                self.workingStack.append(table[state][char])
            elif table[state]['action'] == 'acc':
                # Accept operation, sequence is accepted
                if len(self.inputStack) != 0:
                    raise (Exception('Cannot parse acc'))
                self.workingStack.clear()
            else:
                # Reduce operation on the stack
                reduce_state = int(table[state]['action'].split(' ')[1])
                reduce_production = self.grammar.P[reduce_state]
                to_remove_from_working_stack = [symbol for symbol in reduce_production[1]]
                while len(to_remove_from_working_stack) > 0 and len(self.workingStack) > 0:
                    if self.workingStack[-1] == to_remove_from_working_stack[-1]:
                        to_remove_from_working_stack.pop()
                    self.workingStack.pop()
                if len(to_remove_from_working_stack) != 0:
                    raise (Exception('Cannot Parse reduce'))
                self.inputStack.insert(0, char)
                self.inputStack.insert(0, reduce_production[0])
                self.output.insert(0, reduce_state)

        print('Syntax analysis successfully. Yay!')
        return self.output

    @staticmethod
    def print_canonical_collection(cc):
        """
        Print in a nicer format
        """
        res = "-----------\nCanonical collection: \n"
        for elem in cc:
            res += str(elem) + "\n"
        print(res)
