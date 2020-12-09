import re
from scanner.tables.SymbolTable import SymbolTable
from scanner.program import language_specs
from scanner.program.PIF import ProgramInternalForm


class Scanner:
    def __init__(self, _filename):
        self.pif = ProgramInternalForm()
        self.st = SymbolTable()
        self.filename = _filename

    @staticmethod
    def is_separator(char):
        return char in language_specs.separators

    @staticmethod
    def is_operator(char):
        return char in language_specs.operators

    @staticmethod
    def is_reserved(word):
        return word in language_specs.reservedWords

    @staticmethod
    def is_identifier(word):
        """
        Checks if a string is a correct identifier based on language specs lexical.
        :param word: The string to be checked.
        :return: true or false
        """
        return re.match(r'^[a-zA-Z]([a-zA-Z]|[0-9]){0,8}$', word) is not None

    @staticmethod
    def is_constant(token):
        """
        Verify if its a constant.
        characterConstant = ‘letter‘ | ‘digit’
        integerConstant = [ “+” | “-” ] nonzero_digit {digit} | “0”
        :param token:
        :return: true if its constant, false otherwise
        """
        return re.match(r'((\'[a-zA-Z]\'|\'[0-9]\')|(([+\-])?[1-9]\d*|0)$)', token) is not None

    @staticmethod
    def get_code_of_token(token):
        try:
            return language_specs.codification[token]
        except Exception:
            raise Exception("Error! The token is not in codification table!")

    def tokenize(self):
        """
        Read from the file. Create regex for separators. Tokenize each line.
        :return: List of lists. Tokens from each line
        """
        result = []
        with open(self.filename) as file:
            re_separator = r'('

            # Create a regex for all separators, so it finds them
            for separator in language_specs.separators:
                re_separator += re.escape(separator) + '|'
            re_separator = re_separator[:-1] + ')'

            # Tokenize each line
            for line in file:
                line = line.strip()
                new_line = re.split(re.compile(re_separator), line)
                result.append(new_line)
        return result

    def lexical_analysis(self):
        """
        Main algorithm for returning the completed PIF table along with the SymbolTable.
        After tokenization of the txt file, we parse each token and check if its a constant, reserved keyword, etc.
        If identifier/constant, we add in Symbol Table a record of the new position in its Hash Table.
        """
        errors = ""
        line_number = 0
        lines_array = self.tokenize()
        print("----------- Lexical analysis -----------")
        for line in lines_array:
            line_number += 1
            # print("--------------------\nline: ", line)
            for token in line:
                if token != '' and token != ' ':
                    # print(token)
                    if self.is_reserved(token) or self.is_operator(token) or self.is_separator(token):
                        # print("operator or separator or reserved")
                        self.pif.add(self.get_code_of_token(token), -1)

                    elif self.is_identifier(token):
                        # print("identifier")
                        pos = self.st.add(token)
                        self.pif.add(self.get_code_of_token('identifier'), pos)

                    elif self.is_constant(token):
                        # print("constant")
                        pos = self.st.add(token)
                        self.pif.add(self.get_code_of_token('constant'), pos)
                    else:
                        errors += "Lexical error: line " + str(line_number) + " -> " + ''.join(line) + "\n"

        # Check the lexical correctness
        if errors != "":
            raise Exception(errors)

        self.write_to_file()
        print("Successful lexical analysis.")

    def write_to_file(self):
        """
        Write the PIF to an out file.
        """
        f = open("text_files\\output\\PIF.out", "w")
        for el in self.pif.pif:
            f.write(str(el) + "\n")

    def __str__(self):
        return str(self.pif)
