"""
A class for creating a multi-branch (a parent has one, two, or more children) tree.
Methods:

1. add_son: add a child for the branch
2. have_son: check if there is a certain node in this tree
3. descend: return a certain child of one certain node having certain properties
4. find_node: return a node having certain properties in the tree
5. depth: the depth of the tree
6. find_leaves: return the leaves of a tree
7. count_leaves: return the number of leaves of a tree
8. count_nodes: return number of nodes of a tree
9. is_leaf: whether some certain node is a leaf node
10. squeeze: delete parents with only one child and make the grandparents as the parent
"""

class Node():
    def __init__(self, name, ID, papa = None):
        self.ID = ID     # ImageNet ID
        self.name = name  # ImageNet Name
        self.sons = []    # children
        self.papa = papa  # parent
    
    
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
    
    def find_leaves(self):
        leaf_List = []
        self.find_leaves_R(leaf_List)
        return leaf_List
        
    def find_leaves_R(self, leaf_List = None):
        if leaf_List == None:
            leaf_List = []
        if self.sons == []:
            leaf_List += [self]
            return 1
        else:
            leaves = 0
            for son in self.sons:
                son_leaves = son.find_leaves_R(leaf_List)
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