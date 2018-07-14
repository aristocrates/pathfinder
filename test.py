"""
Tests

Nicholas Meyer
"""
import numpy as np

import structs
from structs import Point, Node, make_forest
from grid import Grid

def squared_distance(tup1, tup2):
    return sum([(k1 - tup2[i])**2 for i, k1 in enumerate(tup1)])

def test_distance():
    """
    Test the squared distance function used in testing the grid
    """
    print("Testing squared distance function")
    p1 = (1, 2, 3)
    p2 = (6, 7, 8)
    assert_same(squared_distance(p1, p2), 75)
    p1 = (0, 0)
    p2 = (3, 4)
    assert_same(squared_distance(p1, p2), 5**2)
    print("All tests passed")
    
def test_grid(random_seed = None):
    if random_seed is None:
        random_seed = np.random.randint(99999999)
    print("Testing grid")
    print("Random seed is: {}".format(random_seed))
    np.random.seed(random_seed)
    test_distance()

    g = Grid(100, 400, 15.2, 4.7)
    allPoints = g.allPoints()
    assert(len(allPoints) == 100 * 400)

    print("Testing bounds")
    assert g.bounds((1, 2))
    assert g.bounds((4.8, 4.6))
    assert g.bounds((0.01, 0.002))
    assert g.bounds((15.19, 4.69))
    assert not g.bounds((4.8, 4.8))
    assert not g.bounds((-1, 3))
    assert not g.bounds((3, -0.01))
    assert not g.bounds((15.3, 4.6))

    print("Testing contains")
    assert g.contains((0, 0))
    assert g.contains((0.000001, -0.000001), neighborhood_thresh = 1e-4)
    assert g.contains((15.2 / 100, 4.7 / 400), neighborhood_thresh = 1e-4)
    assert not g.contains((15.2 * 1.5 / 100, 4.7 / 400),
                          neighborhood_thresh = 1e-4)
    assert not g.contains((15.2 / 100, 4.7 * 1.5 / 400),
                          neighborhood_thresh = 1e-4)
    assert g.contains((15.2, 4.7), neighborhood_thresh = 1e-4)
    # now do a thorough test of all the grid points
    for x_coord in range(101):
        for y_coord in range(401):
            x_iter = 15.2 / 100
            y_iter = 4.7 / 400
            assert g.contains((x_iter * x_coord, y_iter * y_coord),
                              neighborhood_thresh = 1e-4)
            # generate random noise above neighborhood_thresh
            noise_coords_x = [0.101 + 0.798 * np.random.uniform()
                              for k in range(10)]
            noise_coords_y = [0.101 + 0.798 * np.random.uniform()
                              for k in range(10)]
            for x_noise in noise_coords_x:
                for y_noise in noise_coords_y:
                    assert not g.contains((x_iter * (x_coord + x_noise),
                                           y_iter + (y_coord + y_noise)),
                                          neighborhood_thresh = 1e-1)

    print("Testing points within radius straightforward case")
    rad = 1
    select_point = (5, 2)
    points = g.pointsWithinRadius(select_point, rad)
    for p in points:
        assert g.bounds(p)
        assert g.contains(p)
        assert squared_distance(select_point, p) <= rad**2

    print("Testing points within radius edge case")
    rad = 2
    select_point = (15, 4)
    points = g.pointsWithinRadius(select_point, rad)
    for p in points:
        assert g.bounds(p)
        assert g.contains(p)
        assert squared_distance(select_point, p) <= rad**2

    print("Testing enabled points")
    assert len(g.enabledPoints()) == 0
    rad = 1
    select_point = (1, 1)
    points_to_enable = g.pointsWithinRadius(select_point, rad)
    newly_enabled = g.notEnabledIn(points_to_enable)
    g.enablePoints(newly_enabled)
    assert len(points_to_enable) == len(newly_enabled)
    newly_enabled2 = g.notEnabledIn(points_to_enable)
    assert len(newly_enabled2) == 0
    point_append_list = [(4, 4), (3, 3)]
    point_append_list = [g.nearestPoint(k) for k in point_append_list]
    assert len(point_append_list) == len(g.notEnabledIn(point_append_list))
    g.enablePoints(point_append_list)
    assert (len(g.enabledPoints())
            == len(newly_enabled) + len(point_append_list))
    g.clearEnabled()
    assert len(g.enabledPoints()) == 0

    print("Testing disable points")
    num_disable_point_test = 400
    assert num_disable_point_test > 0, ("Error in test file: "
                                        + "num total must be > 0")
    max_repeat_tries = 100
    num_repeats = 0
    repeats_exist = True
    while repeats_exist and num_repeats < max_repeat_tries:
        point_append_list2 = [(np.random.uniform() * g.width,
                               np.random.uniform() * g.height)
                              for k in range(num_disable_point_test)]
        point_append_list2 = [g.nearestPoint(k) for k in point_append_list2]
        # check for repeats and discard and restart if any exist
        # this should be pretty rare
        # (with appropriately sized num_disable_point_test)
        # but will cause test failures if not caught
        repeat_hash = {}
        for p in point_append_list2:
            if p in repeat_hash:
                print("Repeat point found")
                num_repeats += 1
                break
            else:
                repeat_hash[p] = p
        else: # no repeat found
            repeats_exist = False
    if num_repeats >= max_repeat_tries:
        print("Test inconclusive; points repeated too many times")
        print("Try increasing repeat tries or decreasing total number")
        return
    assert len(g.enabledPoints()) == 0
    g.enablePoints(point_append_list2)
    # import pdb; pdb.set_trace()
    # print(len(g.enabledPoints()))
    assert len(g.enabledPoints()) == num_disable_point_test
    num_indices_remove = 30
    assert num_indices_remove > 0, ("Error in test file: num index "
                                    + "to remove must be > 0")
    assert num_indices_remove <= num_disable_point_test, ("Error in test file:"
                                                          + "num index to "
                                                          + "remove must be"
                                                          + " <= num total")
    indices_to_remove = np.random.choice(range(num_disable_point_test),
                                         num_indices_remove,
                                         replace = False)

    for p in point_append_list2:
        assert g.contains(p)
    g.disablePoints([point_append_list2[i] for i in indices_to_remove])
    enabled_post_rm = g.enabledPoints()
    assert len(enabled_post_rm) == (num_disable_point_test
                                    - num_indices_remove)
    for index, p in enumerate(point_append_list2):
        assert g.contains(p)
        if index in indices_to_remove:
            assert p not in enabled_post_rm
        else:
            assert p in enabled_post_rm
    print("All tests passed")

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
