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

    def lookup(self, requestedLocation: str):
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
                    # ambiguous reference, cannot resolve
                    pass
            i += 1
        return None
            
    def put(self, item: str, requestedLocation: str):
        # fetch location
        node = self.lookup(requestedLocation)
        if node != None:
            child = Node(item, node)
            # item DNE
            if item not in self.cache:
                self.cache[item] = [child]
            # item exists, in separate location
            elif item not in map(lambda x: str(x), node.children):
                # collision
                print("-- item collision: " + item)
                self.cache[item].append(child)
            # item exists in this location
            else:
                pass
            
            node.add(child)
            return True
        return False

    def find(self, item: str):
        found = self.lookup(item)
        if found != None:
            path = item
            location = found
            while path.endswith(location.val):
                path = path[:item.find(location.val)].strip()
                location = location.parent
            return [location.val]
        if item in self.cache:
            return list(map(lambda x: str(x.parent), self.cache[item]))
        return None

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
inv.put("apple", "kitchen l my lai")
print(inv)
print("?")
print(inv.find("my lai apple"))
print(inv.find("bed"))