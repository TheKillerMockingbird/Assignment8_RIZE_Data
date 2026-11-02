class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    
    def __init__(self, name, number):
        self.name = name
        self.number = number
    
    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''
   
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''
    
    def __init__(self, size=10):
        self.size = size
        self.data = [None] * size
    
    def hash_function(self, key):
        hash_value = 0
        for char in key:
            hash_value += ord(char)
        return hash_value % self.size
    
    def insert(self, key, value):
        index = self.hash_function(key)
        contact = Contact(key, value)
        new_node = Node(key, contact)
        
        if self.data[index] is None:
            self.data[index] = new_node
            return
        
        current = self.data[index]
        while current is not None:
            if current.key == key:
                current.value.number = value
                return
            if current.next is None:
                current.next = new_node
                return
            current = current.next
    
    def search(self, key):
        index = self.hash_function(key)
        current = self.data[index]
        
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None
    
    def print_table(self):
        for i in range(self.size):
            print(f"Index {i}:", end=" ")
            current = self.data[i]
            if current is None:
                print("Empty")
            else:
                while current is not None:
                    print(f"{current.value}", end="")
                    if current.next is not None:
                        print(" - ", end="")
                    current = current.next
                print()


# Testing section

if __name__ == "__main__":
    table = HashTable(10)
    
    print("Empty table:")
    table.print_table()
    
    # Add some values
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    
    print("\nAfter inserting John and Rebecca:")
    table.print_table()
    
    contact = table.search("John")
    print(f"\nSearch result: {contact}")
    
    # Edge Case #1 – collisions
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    
    print("\nAfter adding Amy and May (possible collision):")
    table.print_table()
    
    # Edge Case #2 – duplicate key (should update)
    table.insert("Rebecca", "999-444-9999")
    
    print("\nAfter updating Rebecca:")
    table.print_table()
    
    # Edge Case #3 – search for something that doesn't exist
    print(f"\nSearch for Chris: {table.search('Chris')}")



# A hash table is the right structure when you need very fast lookups by key. In a normal list you might have to scan every contact one-by-one (O(n) time). In a balanced tree the cost is O(log n). With a good hash function a hash table can average O(1) time for both insert and search, which is ideal for a contact book that will be queried many times.
# I handled collisions with separate chaining. Each slot in the array holds the head of a linked list of Nodes. When two names hash to the same index, the new Node is simply added to the end of that list. When searching, I walk the short list at that index until I find a matching key or reach the end. This approach is simple, uses the Node class we already built, and keeps the average chain length short as long as the table isn’t overloaded.
# An engineer would choose a hash table over a plain list or a tree when the main operations are “look up by exact key” and the data set is large enough that linear or logarithmic time becomes noticeable. Lists are fine for tiny collections or when you need to preserve insertion order. Trees (or sorted lists) are better when you also need range queries or ordered traversal. Hash tables shine when you only care about “get me the value that belongs to this exact key as fast as possible.”