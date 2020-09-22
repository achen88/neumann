class Node:
    def __init__(self, val: str, parent):
        self.val = val
        self.children = []
        self.parent = parent

    def add(self, child):
        self.children.append(child)

    def remove(self, child):
        self.children.remove(child)

    def __str__(self):
        return self.val

class Inventory:
    def __init__(self, file_load=None):
        self.root = Node("root", None)
        self.cache = {"root": [self.root]}

    def lookup(self, requestedLocation):
        words = requestedLocation.split()
        i = 1
        while i <= len(words):
            temp = " ".join(words[-i:])
            if temp in self.cache:
                if len(self.cache[temp]) == 1:
                    return self.cache[temp][0]
                elif " ".join(words[:-i]) != "":
                    parent = self.lookup(" ".join(words[:-i]))
                    if parent != None:
                        for node in self.cache[temp]:
                            if node.parent == parent:
                                return node
                else:
                    pass
            i += 1
        return None
            

    # ignore cache collisions
    def put(self, item: str, location: str):
        # ignore nested locations
        # fetch location
        if location in self.cache and len(self.cache[location]) == 1:
            node = self.cache[location][0]
            child = Node(item, node)
            # item DNE
            if item not in self.cache:
                self.cache[item] = [child]
            # item exists, in separate location
            elif item not in map(lambda x: str(x), node.children):
                # collision
                print("-- item collision")
                self.cache[item].append(child)
            # item exists in this location
            else:
                pass
            
            node.add(child)
            return True
        return False

    def find(self, item: str):
        if item in self.cache:
            return list(map(lambda x: str(x.parent), self.cache[item]))

    def __str__(self):
        string = ""
        for item, nodes in self.cache.items():
            string += item + ": " + " | ".join(map(lambda x: ", ".join(map(lambda y: str(y), x.children)), nodes)) + "\n"
        return string

inv = Inventory()
inv.put("kitchen l", "root")
inv.put("cabinet", "kitchen l")
inv.put("bedroom", "root")
inv.put("bed", "root")
inv.put("bed", "bedroom")
inv.put("my lai", "root")
inv.put("my lai", "kitchen l")
print(inv)
print(inv.lookup("kitchen l my lai").parent)
print(inv.find("bed"))