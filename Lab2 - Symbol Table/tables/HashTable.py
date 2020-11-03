class HashTable:
    """
    A hash table is used to store data in Symbol/Constants table
    """

    def __init__(self):
        self.__content = {}

    def add(self, value):
        """
        Adds a new identifier/constant into the hash table.
        :param value: string
        :return:
        """
        # Hash to get the index where to insert
        key_index = self.__hash(value)

        # Check if there is a record of this key
        if key_index in self.__content.keys():
            collision_list = self.__content[key_index]

            # If we did not encounter this identifier/constant before, we add it
            if value not in collision_list:
                collision_list.append(value)

            return key_index, collision_list.index(value)
        else:
            self.__content[key_index] = [value]
            cl_index = 0
            index = len(self.__content) - 1

        return index, cl_index

    def get_id(self, value):
        """
        Return the index of the searched element
        :param value:
        :return:
        """
        key_index = self.__hash(value)

        # Check if its hash key was found before
        if not(key_index in self.__content.keys()):
            return None

        collision_list = self.__content[key_index]
        # Check if exactly this value was added before
        if value not in collision_list:
            return None

        cl_index = collision_list.index(value)

        return key_index, cl_index

    def __hash(self, value):
        """
        Takes a string of characters, sums up ascii code of every one then returns the sum.
        :param value: identifier, string
        :return: integer
        """
        sum_chars = 0
        for char in value:
            sum_chars += ord(char)

        return sum_chars % 67

    def __str__(self):
        return str(self.__content)
