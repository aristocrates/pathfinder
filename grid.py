"""
Grid overlay on top of map
"""
import numpy as np

class Grid:
    """
    A rectangular array of points
    """
    def __init__(self, num_horiz, num_vert, width = 1, height = 1):
        """
        By default, width and height are normalized to one
        """
        self.num_horiz = num_horiz
        self.num_vert  = num_vert
        self.width     = width
        self.height    = height
        self.x_res     = 1. * self.width / self.num_horiz
        self.y_res     = 1. * self.height / self.num_vert
        self.enabled_points = {}
        self.enabled_points_as_int = {}

    def pointsWithinRadius(self, point, rad):
        x, y = point
        xstart = np.floor( (x - rad) / self.x_res) * self.x_res
        ystart = np.floor( (y - rad) / self.y_res) * self.y_res
        xstart = max(xstart, 0)
        ystart = max(ystart, 0)

        xend   = np.ceil( (x + rad) / self.x_res) * self.x_res
        yend   = np.ceil( (y + rad) / self.y_res) * self.y_res
        xend   = min(xend, self.width)
        yend   = min(yend, self.height)

        numx   = np.round((xend - xstart) / self.x_res) + 1
        numy   = np.round((yend - ystart) / self.y_res) + 1
        grid_x, grid_y = np.meshgrid(np.linspace(xstart, xend, numx),
                                     np.linspace(ystart, yend, numy))
        within_rad = ( (grid_x - x)**2 + (grid_y - y)**2) < rad**2
        return np.column_stack((grid_x[within_rad] ,grid_y[within_rad]))

    def allPoints(self, sparseness = 1):
        xvals, yvals = np.meshgrid(np.linspace(0, self.width,
                                               int(self.num_horiz / sparseness)),
                                   np.linspace(0, self.height,
                                               int(self.num_vert / sparseness)))
        return np.column_stack((xvals.flatten(), yvals.flatten()))

    def notEnabledIn(self, points_list):
        ans = []
        for point in points_list:
            point = tuple(point)
            if self.contains(point) and not point in self.enabled_points:
                ans.append(point)
        return ans

    def enablePoints(self, points_list):
        """
        Sets the points in points_list as enabled
        """
        for point in points_list:
            point = tuple(point)
            if self.contains(point):
                int_point = self.integerPoint(point)
                self.enabled_points[point] = point
                self.enabled_points_as_int[int_point] = int_point

    def integerPoint(self, point):
        x = round(point[0] / self.x_res)
        y = round(point[1] / self.y_res)
        return (x, y)

    def disablePoints(self, points_list):
        for point in points_list:
            point = tuple(point)
            int_point = self.integerPoint(point)
            if point in self.enabled_points:
                self.enabled_points.pop(point)
                assert(int_point) in self.enabled_points_as_int
                self.enabled_points_as_int.pop(int_point)

    def enabledPoints(self):
        return self.enabled_points

    def enabledPointsAsInt(self):
        return self.enabled_points_as_int

    def clearEnabled(self):
        self.enabled_points = {}
        self.enabled_points_as_int = {}

    def bounds(self, point):
        return 0 <= point[0] <= self.width and 0 <= point[1] <= self.height

    def contains(self, point, neighborhood_thresh = 1e-4):
        """
        Returns true if point is within neighborhood_thresh of a grid point

        Note that this can return true for points out of bounds by
        neighborhood_thresh
        """
        x      = point[0] / self.x_res
        y      = point[1] / self.y_res
        xround = round(x)
        yround = round(y)
        if (abs(xround - x) > neighborhood_thresh
            or xround < 0 or xround > self.num_horiz):
            return False
        if (abs(yround - y) > neighborhood_thresh
            or yround < 0 or yround > self.num_vert):
            return False
        return True

    def nearestPoint(self, point):
        x = round(point[0] / self.x_res)
        y = round(point[1] / self.y_res)

        x = max(x, 0)
        y = max(y, 0)
        x = min(x, self.num_horiz)
        y = min(y, self.num_vert)

        x = x * self.x_res
        y = y * self.y_res

        return (x, y)
