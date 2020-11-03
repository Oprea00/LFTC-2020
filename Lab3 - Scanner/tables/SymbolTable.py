from tables.HashTable import HashTable


class SymbolTable:
    """
    Table for identifiers and constants. Has a hash table as field where data is stored.
    """

    def __init__(self):
        self.__hashTable = HashTable()

    def add(self, value):
        return self.__hashTable.add(value)

    def get(self, value):
        return self.__hashTable.get_id(value)

    def __str__(self):
        return str(self.__hashTable)
