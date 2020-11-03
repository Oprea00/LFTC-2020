from program import language_specs
from program.Scanner import Scanner


files = ['p1err.txt', 'p1.txt', 'p2.txt', 'p3.txt']

scanner = Scanner(files[2])
scanner.lexical_analysis()
print(scanner.pif)
print()
print(language_specs.codification)
print("Symbol table: " + str(scanner.st))



'''
// Error: constant cannot start with zero
// Error: invalid identifier name
// Error: '' not closed.

antete functii date rezultate
noua diagrama uml

unar - si aritmetic 7--9
'''
















