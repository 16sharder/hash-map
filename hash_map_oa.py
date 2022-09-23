# Name: Sara Harder
# OSU Email: harders@oregonstate.edu
# Course: CS 261 400 - Data Structures
# Assignment: 6, Open Addressing Hash Map
# Due Date: 06/03/22
# Description: An implementation of a hash map through a pre-created dynamic array class using open addressing.
#              Includes various methods to modify the hash map, without using built-in Python data structures.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Returns nothing. Adds a key with a value to the hash map, or updates the key if it already exists
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair

        # if the load factor is too big, adds more space to the array (thus reducing the load factor)
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # finds the appropriate index using the hash function
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        # if there is no key at that index, adds the new entry to the array
        if self._buckets[index] is None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
            return

        # establishes variables for probing
        to_square = 0
        new_index = index

        # searches the next indices to see if the key already exists
        while self._buckets[new_index] is not None:
            # if the key does exist, updates the value
            if self._buckets[new_index].key == key:
                self._buckets[new_index].value = value
                # if the key was a tombstone, updates the tombstone value and adds to the size
                if self._buckets[new_index].is_tombstone:
                    self._buckets[new_index].is_tombstone = False
                    self._size += 1
                return

            # if the next value is a tombstone value, that tombstone is replaced
            if self._buckets[new_index].is_tombstone:
                self._buckets[new_index] = HashEntry(key, value)
                self._size += 1
                return

            # if the current key is not the target key, moves to next index
            to_square += 1
            new_index = (index + to_square ** 2) % self._capacity

        # if the key doesn't already exist, adds it to the probed index
        self._buckets[new_index] = HashEntry(key, value)
        self._size += 1

    def table_load(self) -> float:
        """
        Returns the current load of the table, the num of elements divided by the num of spaces in the array
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the quantity of array slots that are empty
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Returns nothing. Given a new capacity, resizes the hash table, and re-hashes all the old elements
        """
        if new_capacity < 1 or new_capacity < self._size:
            return

        # saves the old dynamic array
        old_array = self._buckets

        # reassigns the capacity and creates a new Dynamic Array
        self._capacity = new_capacity
        self.clear()

        # for each element in the old array, adds the element to the new array (calling put)
        for index in range(old_array.length()):
            elem = old_array[index]
            if elem is not None and not elem.is_tombstone:
                self.put(elem.key, elem.value)

    def get(self, key: str) -> object:
        """
        Given a key, returns the value of that key if it is in the hash map. Otherwise, returns None
        """
        # calculates which index the key belongs at based on hash function
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        # establishes variables for probing
        entry = self._buckets[index]
        to_square = 0

        # searches the indices to see if the key is in the hash map
        while entry is not None:
            # if found, returns that entry's value
            if entry.key == key and not entry.is_tombstone:
                return entry.value

            # if the entry is found, but it is a tombstone, returns None
            if entry.key == key and entry.is_tombstone:
                return None

            # if not yet found, probes to the next index
            to_square += 1
            new_index = (index + to_square ** 2) % self._capacity
            entry = self._buckets[new_index]

        # if the key does not exist in the hash map, returns None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Given a key, returns True if the key is in the hash map. Otherwise, returns False
        """
        # retrieves the value of the key to determine if the key exists
        elem = self.get(key)

        if elem is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Returns nothing. Given a key, removes the element from the dynamic array and replaces it with a tombstone
        """
        if self._size == 0:
            return

        # if the key is in the array, probes for it, then removes its key and value, replacing it with a tombstone
        if self.contains_key(key):
            hash_val = self._hash_function(key)
            index = hash_val % self._capacity

            # establishes variables for probing
            entry = self._buckets[index]
            to_square = 0
            new_index = index

            # searches the indices until it reaches the desired key
            while entry.key != key:
                # if not yet found, probes to the next index
                to_square += 1
                new_index = (index + to_square ** 2) % self._capacity
                entry = self._buckets[new_index]

            # once found, makes the entry a tombstone
            self._buckets[new_index].is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """"
        Returns nothing. Clears the hash table by creating a new array with new chains
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray created of all the keys in the hash map
        """
        array = DynamicArray()

        # goes through each entry and adds its key to the array
        for index in range(self._buckets.length()):
            entry = self._buckets[index]
            if entry is not None and not entry.is_tombstone:
                array.append(entry.key)

        return array


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
