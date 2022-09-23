# Name: Sara Harder
# OSU Email: harders@oregonstate.edu
# Course: CS 261 400 - Data Structures
# Assignment: 6, Chaining Hash Map
# Due Date: 06/03/22
# Description: An implementation of a hash map through a pre-created dynamic array class using linked list chaining.
#              Includes various methods to modify the hash map, without using built-in Python data structures.
#              Also includes an algorithm to find the mode of a dynamic array.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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

    def find_bucket(self, key):
        """
        Returns the bucket that a key should be found in, based on the hash function
        """
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        bucket = self._buckets[index]
        return bucket

    def put(self, key: str, value: object) -> None:
        """
        Returns nothing. Adds a key with a value to the hash map, or updates the key if it already exists
        """
        # calculates which bucket the key belongs in based on hash function
        bucket = self.find_bucket(key)

        # determines if the key already exists
        elem = bucket.contains(key)
        if elem is not None:
            elem.value = value
            return

        # if the key doesn't exist, adds it to the front of the bucket linked list
        bucket.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the quantity of buckets (linked lists) that are empty
        """
        # if there are no elements in the hash map, all buckets are empty
        if self._size == 0:
            return self._capacity

        counter = 0

        # finds the length of each bucket and determines if it is empty
        for bucket_index in range(self._buckets.length()):
            bucket = self._buckets[bucket_index]
            if bucket.length() == 0:
                counter += 1

        return counter

    def table_load(self) -> float:
        """
        Returns the current load of the table, the num of elements divided by the num of buckets (including empty)
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Returns nothing. Clears the hash table by creating a new array with new chains
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Returns nothing. Given a new capacity, resizes the hash table, and re-hashes all the old elements
        """
        if new_capacity < 1:
            return

        # saves the old dynamic array
        old_buckets = self._buckets

        # reassigns the capacity and creates a new Dynamic Array
        self._capacity = new_capacity
        self.clear()

        # for each bucket in the old array, adds each element in the bucket to the new array (calling put)
        for bucket_index in range(old_buckets.length()):
            bucket = old_buckets[bucket_index]
            for elem in bucket:
                self.put(elem.key, elem.value)

    def get(self, key: str) -> object:
        """
        Given a key, returns the value of that key if it is in the hash map. Otherwise, returns None
        """
        # calculates which bucket the key belongs in based on hash function
        bucket = self.find_bucket(key)

        # determines if the key is not in the hash map
        elem = bucket.contains(key)
        if elem is None:
            return None

        # if the key does exist, returns its value
        return elem.value

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
        Returns nothing. Given a key, removes the node from the appropriate bucket
        """
        if self._size == 0:
            return

        if self.contains_key(key):
            bucket = self.find_bucket(key)
            bucket.remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray created of all the keys in the hash map
        """
        array = DynamicArray()

        # goes through each node in each bucket and adds it to the array
        for bucket_index in range(self._buckets.length()):
            bucket = self._buckets[bucket_index]
            for node in bucket:
                array.append(node.key)

        return array

    def get_buckets_array(self):
        """
        Returns the dynamic array that holds all the buckets
        """
        return self._buckets


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Given an array, returns a tuple with the values that occur most in that array, and the quantity of times they occur
    """
    map = HashMap(da.length() // 3, hash_function_1)

    # creates a hash map which uses the array element as the key, and the number of times it has occurred as the value
    for idx in range(da.length()):
        key = da[idx]
        count = map.get(key)

        # if the element is already in the map, adds 1 to its count
        if count is not None:
            map.put(key, count + 1)

        # if the element is not in the map, adds it to the map with a count of 1
        else:
            map.put(key, 1)

    # initializes the frequency of the mode and the array of modes
    mode_occurrence = 0
    mode_array = DynamicArray()

    buckets_array = map.get_buckets_array()

    # goes through each unique node in each bucket
    for bucket_index in range(buckets_array.length()):
        bucket = buckets_array[bucket_index]
        for node in bucket:

            # if the key has occurred more in the initial array than any previous key
            # updates the mode_occurrence and creates a new mode_array with just this key, eliminating the old
            if node.value > mode_occurrence:
                mode_occurrence = node.value
                mode_array = DynamicArray()
                mode_array.append(node.key)

            # if the key has occurred the same as current mode, adds key to mode_array without eliminating the old
            elif node.value == mode_occurrence:
                mode_array.append(node.key)

            # if the key has occurred less than the current mode, nothing happens and moves to next key

    tuple = (mode_array, mode_occurrence)
    return tuple


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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
