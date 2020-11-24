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
        What a state contains
        In: productions, the list of productions for closure
        Out: closure
        """
        if not productions:
            return None

        # initialise Closure with productions
        closure = productions

        done = False
        while not done:  # while we add a dotted production to the closure
            done = True

            # search productions with dot in front of non-terminal
            for dotted_prod in closure:
                dot_index = dotted_prod[1].index('.')
                alpha = dotted_prod[1][:dot_index]
                Bbeta = dotted_prod[1][dot_index + 1:]
                if len(Bbeta) == 0:
                    continue
                B = Bbeta[0]
                if B in self.grammar.E:
                    continue

                # search productions of that non-terminal
                for prod in self.grammar.getProductions(B):
                    # adds item formed from production with dot in front of right hand side of the production
                    dotted_prod = (B, ['.'] + prod)

                    if dotted_prod not in closure:
                        closure += [dotted_prod]
                        done = False
        return closure

    def go_to(self, state, symbol):
        """
        Move from a state to another.
        In: state, symbol - String
        out: state
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
        Construct set of states.
        state corresponding to prod. of S’ = initial state
        In:
        Out: Collection of states
        """
        # initialise collection with S0
        C = [self.closure([('S1', ['.', self.grammar.S[0]])])]

        finished = False
        while not finished:  # while we add a new state to the collection
            finished = True

            for state in C:
                for symbol in self.grammar.N + self.grammar.E:
                    next_state = self.go_to(state, symbol)
                    if next_state is not None and next_state not in C:
                        # add new state
                        C += [next_state]
                        finished = False

        print(C)
        return C
