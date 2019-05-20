class Node():
    def __init__(self, name, ID, papa = None):
        self.ID = ID
        self.name = name
        self.sons = []
        self.papa = papa
    
    def find_name(nameDict):
        return nameDict[self.ID]
    
    def add_son(self, name = None, ID = None):
        if not self.have_son(name = name, ID = ID):
            son = Node(name = name, ID = ID, papa = self)
            self.sons += [son]
    
    def have_son(self, name = None, ID = None):
        if name:
            for son in self.sons:
                if son.name == name:
                    return True
            return False
        else:
            for son in self.sons:
                if son.ID == ID:
                    return True
            return False
    
    def descend(self, name = None, ID = None):
        if name:
            for son in self.sons:
                if son.name == name:
                    return son
            raise NameError('No this son!')
        else:
            for son in self.sons:
                if son.ID == ID:
                    return son
            raise NameError('No this son!')
            
    def find_node(self, ID = None, name = None):
        if self.name == name or self.ID == ID:
            return self
        if self.sons == []:
            return None
        else:
            for son in self.sons:
                found = son.find_node(ID = ID, name = name)
                if found:
                    return found
            return None
        
    def depth(self):
        if self.sons == []:
            return 1
        else:
            max_depth = 0
            for son in self.sons:
                son_depth = son.depth()
                if son_depth > max_depth:
                    max_depth = son_depth
            return max_depth + 1
    
    def find_leaves(self, leaf_List = None):
        if leaf_List == None:
            leaf_List = []
        if self.sons == []:
            leaf_List += [self.name]
            return 1
        else:
            leaves = 0
            for son in self.sons:
                son_leaves = son.find_leaves(leaf_List)
                leaves += son_leaves
            return leaves
        
    def count_leaves(self):
        if self.sons == []:
            return 1
        else:
            leaves = 0
            for son in self.sons:
                son_leaves = son.count_leaves()
                leaves += son_leaves
            return leaves
    
    def count_nodes(self):
        if self.sons == []:
            return 1
        else:
            nodes = 1
            for son in self.sons:
                son_nodes = son.count_nodes()
                nodes += son_nodes
            return nodes
    
    def is_leaf(self, ID = None, name = None):
        if self.sons == []:
            if self.name == name or self.ID == ID:
                return True
            else:
                return False
        else:
            is_true = False
            for son in self.sons:
                son_true = son.is_leaf(ID, name)
                is_true = is_true or son_true
            return is_true
        
    def squeeze(self):
        if self.sons == []:
            return
        else:
            if len(self.sons) == 1:
                only_child = self.sons[0]
                self.papa.sons += [only_child]
                only_child.papa = self.papa
                self.papa.sons.remove(self)
                only_child.squeeze()
            else:
                for son in self.sons:
                    son.squeeze()