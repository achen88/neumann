class Node:
    def __init__(self, val: str):
        self.val = val
        self.children = []

    def add(self, child):
        self.children.append(child)

    def remove(self, child):
        self.children.remove(child)

    def __str__(self):
        return self.val

class Inventory:
    def __init__(self, file_load=None):
        self.root = Node("root")
        self.cache = {"root": self.root}
    # def lookup(self, location):

    # ignore cache collisions
    def put(self, item: str, location: str):
        # ignore nested locations
        # fetch location
        if location in self.cache:
            node = self.cache[location]
            # item DNE
            if item not in self.cache:
                child = Node(item)
                node.add(child)
                self.cache[item] = child
            # item exists, in separate location
            elif item not in map(lambda x: str(x), node.children):
                # collision
                print("-- item collision")
                pass
            # item exists in this location
            else:
                pass

    def __str__(self):
        string = ""
        for item, node in self.cache.items():
            string += item + ": " + ", ".join(map(lambda x: str(x), node.children)) + "\n"
        return string

inv = Inventory()
inv.put("kitchen", "root")
inv.put("bedroom", "root")
inv.put("bed", "root")
inv.put("bed", "bedroom")
print(inv)