class ParserOutput:
    """
    transform parsing tree into representation;
    print DS to screen and to file
    """

    def __init__(self, parser):
        self.parser = parser

    def derivations_string(self, output_parser):
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

    def print_to_console(self, output_parser):
        """
        Print derivations string to console
        """
        print("Derivation strings: ", self.derivations_string(output_parser))

    def write_to_file(self, output_parser, filename):
        """
        Write derivations string to file.
        If filename is g1.txt then output should be 'out1.txt'.
        """
        if filename == "text_files/grammars/g1.txt":
            f = open("text_files\\output\\out1.txt", "w")
        elif filename == "text_files/grammars/g2.txt":
            f = open("text_files\\output\\out2.txt", "w")
        else:
            raise Exception("Invalid file name for parser output!")

        for el in self.derivations_string(output_parser):
            f.write(str(el) + "\n")
