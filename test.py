"""
A testing module.

Nicholas Meyer
"""
import structs
from structs import Point, Node, make_forest

def test_link():
    print("Testing single link")
    a = Node(Point(1, 1))
    b = Node(Point(4, 5))
    a.link(b)
    assert(len(a.neighbor_list()) == 1)
    assert(len(b.neighbor_list()) == 1)
    assert(a.neighbor_list()[0].loc() == b.loc())
    assert(b.neighbor_list()[0].loc() == a.loc())

    print("Testing multilink")
    c = Node(Point(3, 8))
    d = Node(Point(-3, 9))
    a.link(c)
    a.link(d)
    b.link(c)
    c.link(d)
    assert(len(a.neighbor_list()) == 3)
    a_neighbor_list_locs = [k.loc() for k in a.neighbor_list()]
    assert(b.loc() in a_neighbor_list_locs)
    assert(c.loc() in a_neighbor_list_locs)
    assert(d.loc() in a_neighbor_list_locs)
    assert(len(b.neighbor_list()) == 2)
    b_neighbor_list_locs = [k.loc() for k in b.neighbor_list()]
    assert(a.loc() in b_neighbor_list_locs)
    assert(c.loc() in b_neighbor_list_locs)
    assert(len(c.neighbor_list()) == 3)
    c_neighbor_list_locs = [k.loc() for k in c.neighbor_list()]
    assert(a.loc() in c_neighbor_list_locs)
    assert(b.loc() in c_neighbor_list_locs)
    assert(d.loc() in c_neighbor_list_locs)
    assert(len(d.neighbor_list()) == 2)
    d_neighbor_list_locs = [k.loc() for k in d.neighbor_list()]
    assert(a.loc() in d_neighbor_list_locs)
    assert(c.loc() in d_neighbor_list_locs)

def assert_same(a, b, threshold = 1e-10):
    assert(abs(a - b) < threshold)

def test_dist():
    assert_same(Point(1, 2).dist(Point(0, 0))**2, 5)
    assert_same(Point(-2, 2).dist(Point(0, 0))**2, 8)
    assert_same(Point(3, 4).dist(Point(0, 0))**2, 25)
    assert_same(Point(-3, 4).dist(Point(0, 0))**2, 25)
    assert_same(Point(5, 12).dist(Point(0, 0))**2, 13**2)

close_point = [Point(1, 2), Point(-3, 4), Point(2, -1), Point(2, 3),
               Point(5, -8), Point(-9, 0), Point(-3, 3), Point(9, 2),
               Point(-5, -9), Point(1, -8), Point(-9, 8), Point(4, -7),
               Point(-8, 0), Point(-4, 7), Point(-6, 2), Point(-2, 2),
               Point(9, -2), Point(6, 4), Point(7, 6), Point(9, 7),
               Point(1, -5), Point(-10, -6)]
# construct an arbitrary tree structure for these test points
close_data = [Node(p) for p in close_point]
for i, n in enumerate(close_data):
    n.link(close_data[i - 1])

def test_closest_node():
    """
    Tests the closest_node function
    """
    print("Testing default Point(0, 0) origin")
    for root in close_data:
        closest_node = structs.closest_node(root)
        assert(closest_node.loc() == Point(1, 2))
    custom_origin = Point(-9, 7)
    print("Testing origin of %s" % str(custom_origin))
    for root in close_data:
        closest_node = structs.closest_node(root, custom_origin)
        assert(closest_node.loc() == Point(-9, 8))

forest_data_lite = [Point(1, 1), Point(1, 2), Point(2, 3), Point(4, 5),
                    Point(8, 9), Point(9, 10), Point(9, 11)]
        
forest_data = [Point(1, 5), Point(2, 4), Point(2, 5), Point(2, 6), Point(3, 3),
               Point(3, 4), Point(3, 5), Point(4, 2), Point(4, 3), Point(4, 4),
               Point(4, 5), Point(4, 7), Point(4, 8), Point(5, 1), Point(5, 2),
               Point(5, 3), Point(5, 7), Point(5, 8), Point(5, 9), Point(6, 1),
               Point(6, 2), Point(6, 3), Point(6, 7), Point(6, 8), Point(6, 9),
               Point(7, 2), Point(7, 3), Point(7 ,4), Point(7, 8), Point(7, 9),
               Point(8, 2), Point(8, 3), Point(8, 4), Point(8, 5), Point(8, 6),
               Point(8, 8), Point(8, 9), Point(9, 3), Point(9, 4), Point(9, 5),
               Point(9, 6), Point(9, 7), Point(9, 8), Point(9, 9),
               Point(10, 2), Point(10, 3), Point(10, 4), Point(10, 6),
               Point(10, 7), Point(10, 8), Point(11, 2)]

def test_make_forest():
    """
    Tests the make forest function
    """
    print("Preliminary test")
    forest_lite = make_forest(forest_data_lite)
    forest_lite_actual_locs = [Point(1, 1), Point(4, 5), Point(8, 9)]
    assert(len(forest_lite) == 3)
    forest_lite_locs = [n.loc() for n in forest_lite]
    for loc in forest_lite_actual_locs:
        assert(loc in forest_lite_locs)

    print("Extensive test")
    forest = make_forest(forest_data)

def test_union_find():
    """
    Tests the union find data structure
    """
    print("Creating union structure")
    u = structs.Union()
    print("Making roots")
    for i in range(10):
        u.make(i)
    # connect the evens
    print("Connecting evens")
    for i in range(0, 10, 2):
        u.union(i, 0)
    # connect the odds
    print("Connecting odds")
    for i in range(1, 10, 2):
        u.union(i, 1)

    print("Asserting connections")
    for i in range(0, 10):
        assert(u.find(i) == u.find(i))
        if i < 9:
            assert(u.find(i) != u.find(i + 1))
    assert(u.find(0) == u.find(2))
    assert(u.find(2) == u.find(4))
    assert(u.find(4) == u.find(6))
    assert(u.find(6) == u.find(8))
    assert(u.find(1) == u.find(3))
    assert(u.find(3) == u.find(5))
    assert(u.find(5) == u.find(7))
    assert(u.find(7) == u.find(9))
    print("All tests passed")
