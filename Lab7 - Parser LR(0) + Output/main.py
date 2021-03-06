from parser_algorithm.Grammar import Grammar
from parser_algorithm.Parser import Parser
from parser_algorithm.ParserOutput import ParserOutput
from scanner.program import language_specs
from scanner.program.Scanner import Scanner

# Read Grammar from file
text_file_grammar = 'text_files/grammars/g2.txt'
grammar = Grammar.read_from_file(text_file_grammar)
cmd = 0
while cmd != 0:
    Grammar.print_command_grammar()
    try:
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
        else:
            break
    except ValueError:
        print()
        break

try:
    # Scanner
    uri = 'text_files/code/'
    files = [uri + 'p1err.txt', uri + 'p1.txt', uri + 'p2.txt', uri + 'p3.txt', uri + 'test.txt']
    scanner = Scanner(files[4])
    scanner.lexical_analysis()
    print("PIF: ", scanner.pif)

    # Create reverse lang_specs and prepare stack for the Parser
    reverse_codification = {}
    for key in language_specs.codification:
        reverse_codification[language_specs.codification[key]] = key
    inputStack = []
    for (code, elem_id) in scanner.pif.pif:
        inputStack += [str(code)]
    print()

    # Parser
    parser = Parser(grammar)
    output_parser = []
    if text_file_grammar == 'text_files/grammars/g2.txt':
        output_parser = parser.parse(inputStack)
    elif text_file_grammar == 'text_files/grammars/g1.txt':
        output_parser = parser.parse('aabb')
    else:
        raise Exception("Invalid grammar file name!")

    # Print output from parsing
    parserOutput = ParserOutput(parser)
    print(output_parser)
    parserOutput.print_to_console(output_parser)
    parserOutput.write_to_file(output_parser, text_file_grammar)

except Exception as ex:
    print(ex)
