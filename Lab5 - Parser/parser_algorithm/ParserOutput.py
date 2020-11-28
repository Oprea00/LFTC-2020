class ParserOutput:
    """
    transform parsing tree into representation;
    print DS to screen and to file
    """

    def __init__(self, parser):
        self.parser = parser

    def derivation_strings(self, output_parser):
        """
        Takes a list containing production rules needed to apply to
        obtain the input string. List of derivations. (right most derivation)
        :return: results - list of production rules read from grammar
        """
        result = []
        for el in output_parser:
            production = self.parser.grammar.P[el]
            result.append(production)
        return result

    def print_to_console(self):
        """

        """

    def write_to_file(self):
        """

        """