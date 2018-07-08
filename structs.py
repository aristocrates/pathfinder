"""
Module of data structures to use for the application

Ideally these will be sorted into more organized modules, but for now they are
all here in this utilities-like module due to lack of imagination.

Nicholas Meyer
"""

import numpy as np

class Point:
    """
    Encapsulates a two dimensional point (x, y)

    Sortable by python's comparison for tuples
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def dist(self, p):
        """Applies the distance formula between two points"""
        return ((self.x - p.x)**2 + (self.y - p.y)**2)**0.5

    def get_str(self):
        """The string representation of the Point"""
        return "Point(%s, %s)" % (str(self.x), str(self.y))
    
    def __hash__(self):
        """Hash value for points (same as hash of length 2 tuples)"""
        return hash( (self.x, self.y) )
    
    def __eq__(self, p):
        """@return True if equal, otherwise False"""
        return (self.x, self.y) == (p.x, p.y)
    
    def __str__(self):
        return self.get_str()

    def __repr__(self):
        return self.get_str()

    def __lt__(self, p):
        return (self.x, self.y) < (p.x, p.y)
    
    def __le__(self, p):
        return (self.x, self.y) <= (p.x, p.y)

    def __ne__(self, p):
        return (self.x, self.y) != (p.x, p.y)

    def __gt__(self, p):
        return (self.x, self.y) > (p.x, p.y)

    def __ge__(self, p):
        return (self.x, self.y) >= (p.x, p.y)

class Node:
    """
    Encapsulates the nodes of a graph.

    Stores the graph by adjacency lists.
    """
    def __init__(self, p):
        self._neighbors = {}
        self._loc = p
        self._marked = False
        self._val = -1

    def get_str(self):
        return "Node(%s)" % str(self.loc())

    def loc(self):
        return self._loc

    def set_marked(self, marked):
        self._marked = marked

    def is_marked(self):
        return self._marked

    def set_val(self):
        return self._val

    def get_val(self, val):
        self._val = val

    def neighbors(self):
        return self._neighbors

    def neighbor_list(self):
        return [self._neighbors[k] for k in self._neighbors.keys()]

    def weight(self, n):
        return self.loc().dist(n.loc())

    def __str__(self):
        return self.get_str()

    def __repr__(self):
        return self.get_str()

    def _is_linked(self, n):
        """Gets whether or not a link already exists to node n"""
        try:
            self._neighbors[n.loc()]
            return True
        except KeyError:
            return False

    def link(self, n):
        """Link this node to another. Adds n to neighbors and this to n's
        neighbors.
        @param n    other node to link to
        """
        self._neighbors[n.loc()] = n
        n._neighbors[self.loc()] = self

class Union:
    """
    Implements a union find data structure on arbitrary objects

    Also keeps track of distinct roots

    Written while referencing
    https://en.wikipedia.org/wiki/Disjoint-set_data_structure
    """
    class Wrapper:
        def __init__(self, obj):
            self.value = obj
            self.parent = None
            self.rank = 0

        def __eq__(self, other_wrapper):
            return (self.value == other_wrapper.value
                    and self.rank == other_wrapper.rank)

        def get_parent(self):
            return self.parent

        def get_rank(self):
            return self.rank

        def set_parent(self, parent):
            """
            parent has type Wrapper(obj)
            """
            self.parent = parent

        def set_rank(self, rank):
            """
            rank has type integer
            """
            self.rank = rank

    def __init__(self):
        self.objects = {}
            
    def make(self, x):
        """
        Makes a new set containing just element x

        Returns 0 if no error, 1 if error
        """
        try:
            x_wrap = self.objects[x]
            import sys
            print("Object " + str(x) + " already in tree", file = sys.stderr)
            return 1
        except KeyError:
            self.objects[x] = self.Wrapper(x)
            self.objects[x].set_parent(self.objects[x])
            self.objects[x].set_rank(0)
            return 0

    def union(self, x, y):
        """
        Connects elements x and y

        Raises ValueError if either have not been added yet
        """
        x_root = self.find(x)
        y_root = self.find(y)

        if x_root == y_root:
            return

        x_root = self.objects[x_root]
        y_root = self.objects[y_root]
        if x_root.rank < y_root.rank:
            x_root.set_parent(y_root)
        elif x_root.rank > y_root.rank:
            y_root.set_parent(x_root)
        else:
            y_root.parent = x_root
            x_root.set_rank(x_root.get_rank() + 1)

    def find(self, x):
        """
        Gets to the root of element x, of type Wrapper(obj)
        """
        try:
            x_wrap = self.objects[x]
        except KeyError:
            raise ValueError("element %s has not been added to the tree"
                             % x)
        if x_wrap.get_parent().value != x_wrap.value:
            # flattening of the tree for improved amortized time complexity
            x_wrap.set_parent(self.objects[self.find(x_wrap.get_parent().value)])
        assert(x_wrap.get_parent().value ==
               x_wrap.get_parent().get_parent().value)
        return x_wrap.get_parent().value

class PairingHeap:
    """
    With reference to
    https://www.cise.ufl.edu/~sahni/dsaaj/enrich/c13/pairing.htm
    """
    class Wrapper_node:
        def __init__(self, val):
            pass
    def __init__(self):
        self.root = None
        self.size = 0

    def get_min(self):
        return self.root.value

    def is_empty(self):
        return self.size == 0

    def merge(self, tree):
        pass
    def remove(self, val):
        pass
    def put(self, val):
        pass
    def decrease_key(self):
        pass
    def delete_min(self):
        pass
def neighboring_points(p):
    """
    Gets the 8 integer points surrounding p
    """
    points = [(p.x - 1, p.y - 1), (p.x - 1, p.y), (p.x - 1, p.y + 1),
              (p.x, p.y - 1), (p.x, p.y + 1),
              (p.x + 1, p.y - 1), (p.x + 1, p.y), (p.x + 1, p.y + 1)]
    return [Point(*p) for p in points]

def set_all_marked(nodes_list, value):
    """
    Sets the marked value of every node in the list to value
    """
    for node in nodes_list:
        node.set_marked(value)

def depth_first_list(root, unmark_visited = True):
    """
    Gets a list of all nodes in a depth first search from root.

    Note that if any nodes are marked prior to calling this,
    they will be assumed to already be visited, and these nodes will
    not be unmarked regardless of unmark_visited.
    """
    ans = []
    depth_first_list_recurse(root, ans)
    if unmark_visited:
        set_all_marked(ans, False)
    return ans

def depth_first_list_recurse(node, lst):
    lst.append(node)
    node.set_marked(True)
    for n in node.neighbor_list():
        if not n.is_marked():
            depth_first_list_recurse(n, lst)

def closest_node(root, reference = Point(0, 0)):
    nodes_list = depth_first_list(root)
    
    smallest_node = root
    smallest_distance = reference.dist(root.loc())
    for node in nodes_list:
        temp_dist = reference.dist(node.loc())
        if temp_dist < smallest_distance:
            smallest_node = node
            smallest_distance = temp_dist
        elif temp_dist == smallest_distance:
            if node.loc() < smallest_node.loc():
                # smallest_distance stays the same
                smallest_node = node

    return smallest_node

def make_forest(point_list):
    """Make a tree out of the list of points, where points are defined as
    connected if either their x coordinates or y coordinates or both differ
    by no more than 1.
    Example:

    Running make_forest([Point(1, 1), Point(1, 2), Point(2, 3), Point(4, 5),
          Point(8, 9), Point(9, 10), Point(9, 11)])
    would return a list of size three with root nodes Point(1, 1),
    Point(2, 3), and Point(8, 9) containing trees connected by this rule.

    For the purpose of convention, the point closest to the origin is the
    root for all trees.

    @param point_list    list of points
    @return              a list of root nodes, each representing a connected
                         graph
    """
    # first put every point into a hash and union
    forest = {p:Node(p) for p in point_list}
    forest_connections = Union()
    for p in forest.keys():
        forest_connections.make(p)
    # for each point link all neighbors
    for p in forest.keys():
        for point_link in neighboring_points(p):
            try:
                node_link = forest[point_link]
            except KeyError:
                # if the node isn't in the graph, skip
                continue
            current_node = forest[p]
            if not current_node._is_linked(node_link):
                current_node.link(node_link)
                forest_connections.union(current_node.loc(),
                                         node_link.loc())

    # get all unique roots
    forest_hash = {}
    for point in forest.keys():
        root = forest_connections.find(point)
        try:
            forest_hash[root]
        except KeyError:
            forest_hash[root] = forest[root]

    # traverse every tree depth first, identify closest to origin
    # then set that as the root of each
    roots = []
    for key in forest_hash.keys():
        roots.append(closest_node(forest_hash[key]))

    return roots
