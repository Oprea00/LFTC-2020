class Parser:
    """
    The LR(0) parser algorithm.
    """

    def __init__(self, grammar):
        self.grammar = grammar
        self.workingStack = []
        self.inputStack = []
        self.output = []

