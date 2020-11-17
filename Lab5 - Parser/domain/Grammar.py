import re


class Grammar:
    """
    Grammar used by the parse tree to check all possible combinations of
    syntax statements.
    """

    def __init__(self, N, E, P, S):
        """
        :param N: non terminals
        :param E: terminals
        :param S: starting non-terminal/symbol
        :param P: productions
        """
        self.N = N
        self.E = E
        self.P = P
        self.S = S

    @staticmethod
    def read_from_file(filename):
        """
        Read grammar from file. Domain sets are between '= {..}' and productions
        are separated with '|'.
        :param filename: Text file from local machine.
        :return: Grammar object constructed.
        """
        with open(filename) as file:
            N = Grammar.parse_line(file.readline())
            E = Grammar.parse_line(file.readline())
            S = Grammar.parse_line(file.readline())
            P = Grammar.parse_productions(Grammar.parse_line(''.join([line for line in file])))
        return Grammar(N, E, P, S)

    @staticmethod
    def parse_line(line):
        """
        Used in reading from file the initial domain sets: N, E, S
        :param line:
        :return: List of characters.
        ex: ['S', 'A', 'B']
        """
        return [element.strip() for element in line.strip().split('=')[1].strip()[1:-1].split(',')]

    @staticmethod
    def parse_productions(productions):
        """
        Used in reading from file one line from production rules.
        Parses strings and extracts data between characters '->' and '|'.
        :param productions: List with strings. Production rules from one line of the form
        ex: ['S -> aA | bB', 'A -> aA | bB | aS']
        :return: List of tuples. Each production rule separate by '|' is a tuple.
        ex: [('S', 'aA'), ('S', 'bB'), ('A', 'aA'), ('A', 'bB')]
        """
        result = []
        for rule in productions:
            [lhs, rhs] = rule.strip().split('->')
            results = rhs.strip().split('|')
            for res in results:
                result.append((lhs.strip(), res.strip()))
        return result

    def get_productions(self, symbol):
        """
        Return productions of a non-terminal symbol.
        :param symbol: Non terminal symbol. Capital letter.
        :return: List of strings. Its productions, example S -> ['aA', 'bB']
        """
        result = []
        for production in self.P:
            if production[0] == symbol:
                result.append(production[1])
        return result

