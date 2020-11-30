operators = ['+', '-', '*', '/', '=', '<', '>',
             '<=', '==', '>=', '!=', '&&', '||']
separators = [';', '{', '}', '(', ')', ' ', '\n', '[', ']', ',']
reservedWords = ['int', 'char', 'if', 'else', 'while',
                 'read', 'print', 'list', 'int_main', 'return']
all_alphabet = operators + separators + reservedWords
codification = {all_alphabet[i]: i + 2 for i in range(0, len(all_alphabet))}
codification['identifier'] = 0
codification['constant'] = 1
# print('Codification: \n', codification)
