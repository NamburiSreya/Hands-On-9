import math

class ListNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.forward = None
        self.backward = None

class HashContainer:
    def __init__(self, initial_capacity=8):
        self.bucket_count = initial_capacity
        self.element_count = 0
        self.buckets = [None] * self.bucket_count

    def compute_hash(self, key):
        golden_ratio = 0.6180339887
        product = key * golden_ratio
        fractional_part = product - math.floor(product)
        return int((self.bucket_count * fractional_part)) % self.bucket_count

    def adjust_capacity(self, new_bucket_count):
        new_buckets = [None] * new_bucket_count
        for bucket in self.buckets:
            current = bucket
            while current:
                next_node = current.forward
                new_index = self.compute_hash(current.key)
                current.forward = new_buckets[new_index]
                current.backward = None
                if new_buckets[new_index]:
                    new_buckets[new_index].backward = current
                new_buckets[new_index] = current
                current = next_node
        self.buckets = new_buckets
        self.bucket_count = new_bucket_count

    def add_element(self, key, value):
        if self.element_count >= self.bucket_count:
            self.adjust_capacity(self.bucket_count * 2)

        index = self.compute_hash(key)
        new_node = ListNode(key, value)
        new_node.forward = self.buckets[index]
        if self.buckets[index]:
            self.buckets[index].backward = new_node
        self.buckets[index] = new_node
        self.element_count += 1

    def delete_element(self, key):
        index = self.compute_hash(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                if current.backward:
                    current.backward.forward = current.forward
                else:
                    self.buckets[index] = current.forward
                if current.forward:
                    current.forward.backward = current.backward
                self.element_count -= 1

                if self.element_count <= self.bucket_count // 4 and self.bucket_count > 8:
                    self.adjust_capacity(self.bucket_count // 2)
                return
            current = current.forward

    def find_element(self, key):
        index = self.compute_hash(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.data
            current = current.forward
        return None  # Key not found

    def get_element_count(self):
        return self.element_count

    def get_bucket_count(self):
        return self.bucket_count

# Test the HashContainer
if __name__ == "__main__":
    hash_container = HashContainer()

    # Add some key-value pairs
    hash_container.add_element(5, 50)
    hash_container.add_element(15, 150)
    hash_container.add_element(25, 250)

    # Find and print values
    print(f"Value for key 5: {hash_container.find_element(5)}")
    print(f"Value for key 15: {hash_container.find_element(15)}")
    print(f"Value for key 25: {hash_container.find_element(25)}")

    # Remove a key
    hash_container.delete_element(15)

    # Try to find the removed key
    print(f"Value for key 15 after removal: {hash_container.find_element(15)}")

    # Add many elements to test resizing
    for i in range(100):
        hash_container.add_element(i, i * 10)

    print(f"Final element count: {hash_container.get_element_count()}")
    print(f"Final bucket count: {hash_container.get_bucket_count()}")