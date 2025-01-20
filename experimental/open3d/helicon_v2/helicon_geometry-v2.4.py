# add spheres to intersections within the cube of projection lines
import open3d as o3d
import numpy as np
from math import pi, cos, sin

def find_3d_intersection_point(p1_xy, p1_yz, p1_xz):
    """Calculate the 3D intersection point from three perpendicular projections."""
    # Extract coordinates from each face's point
    x = p1_xy[0]  # x from xy-plane point
    y = p1_xy[1]  # y from xy-plane point
    z = p1_xz[2]  # z from xz-plane point
    return np.array([x, y, z])

def create_cube_faces():
    # Create a unit cube centered at origin
    points = np.array([
        # Front face (xy-plane at z=1)
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1],
        # Right face (yz-plane at x=1)
        [1, -1, -1], [1, 1, -1], [1, 1, 1], [1, -1, 1],
        # Top face (xz-plane at y=1)
        [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]
    ])

    lines = [[0, 1], [1, 2], [2, 3], [3, 0],  # Front face
             [4, 5], [5, 6], [6, 7], [7, 4],  # Right face
             [8, 9], [9, 10], [10, 11], [11, 8]]  # Top face

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.paint_uniform_color([0.5, 0.5, 0.5])

    return line_set

def transform_point(point, plane):
    """Transform a point based on the target plane."""
    if plane == 'xy':  # Front face
        return np.array([point[0], point[1], 1])
    elif plane == 'yz':  # Right face
        return np.array([1, point[0], point[1]])
    elif plane == 'xz':  # Top face
        return np.array([point[0], 1, point[1]])

def create_helicon_pattern(plane='xy', intersection_points_3d=None):
    geometries = []

    # Base circle
    circle_points = []
    for i in range(50):
        theta = 2 * pi * i / 49
        point = [cos(theta), sin(theta)]
        transformed_point = transform_point(point, plane)
        circle_points.append(transformed_point)

    circle = o3d.geometry.LineSet()
    circle.points = o3d.utility.Vector3dVector(circle_points)
    circle.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(49)])
    circle.paint_uniform_color([0, 0, 1])  # Blue
    geometries.append(circle)

    # Original intersection points (scaled to unit cube)
    points_2d = [
        # Central axis points
        [0, 0.5], [0, -0.5], [0.5, 0], [-0.5, 0],
        # Left side clusters
        [-0.6, 0.2], [-0.6, -0.2], [-0.333, 0.333], [-0.333, -0.333],
        [-0.2, 0.6], [-0.2, -0.6],
        # Right side clusters
        [0.6, 0.2], [0.6, -0.2], [0.333, 0.333], [0.333, -0.333],
        [0.2, 0.6], [0.2, -0.6]
    ]

    # Create spheres for intersection points and their projections
    for point_2d in points_2d:
        point_3d = transform_point(point_2d, plane)

        # Original point sphere
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
        sphere.translate(point_3d)
        sphere.paint_uniform_color([0.5, 1, 0.5])  # Light green
        geometries.append(sphere)

        # Create projection line
        if plane == 'xy':
            end_point = point_3d - [0, 0, 2]
        elif plane == 'yz':
            end_point = point_3d - [2, 0, 0]
        else:  # xz
            end_point = point_3d - [0, 2, 0]

        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector([point_3d, end_point])
        line.lines = o3d.utility.Vector2iVector([[0, 1]])
        line.paint_uniform_color([0.8, 0.8, 0.8])  # Light gray
        geometries.append(line)

    # Add purple spheres at 3D intersection points if provided
    if intersection_points_3d is not None:
        for point in intersection_points_3d:
            sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
            sphere.translate(point)
            sphere.paint_uniform_color([0.7, 0, 1.0])  # Purple
            geometries.append(sphere)

    return geometries

def calculate_3d_intersections(points_2d):
    """Calculate where three perpendicular projections intersect."""
    intersections = []

    # For each point, find its corresponding projections on other faces
    for point in points_2d:
        # Transform point to each face
        p_xy = transform_point(point, 'xy')
        p_yz = transform_point(point, 'yz')
        p_xz = transform_point(point, 'xz')

        # Calculate intersection point
        intersection = find_3d_intersection_point(p_xy, p_yz, p_xz)
        if np.all(np.abs(intersection) <= 1):  # Only keep points inside cube
            intersections.append(intersection)

    return intersections

def visualize_3d_helicon():
    geometries = []

    # Calculate 3D intersection points
    points_2d = [
        # Central axis points
        [0, 0.5], [0, -0.5], [0.5, 0], [-0.5, 0],
        # Left side clusters
        [-0.6, 0.2], [-0.6, -0.2], [-0.333, 0.333], [-0.333, -0.333],
        [-0.2, 0.6], [-0.2, -0.6],
        # Right side clusters
        [0.6, 0.2], [0.6, -0.2], [0.333, 0.333], [0.333, -0.333],
        [0.2, 0.6], [0.2, -0.6]
    ]

    intersection_points_3d = calculate_3d_intersections(points_2d)

    # Add cube faces
    geometries.append(create_cube_faces())

    # Add Helicon pattern to three faces with 3D intersections
    geometries.extend(create_helicon_pattern('xy', intersection_points_3d))
    geometries.extend(create_helicon_pattern('yz', intersection_points_3d))
    geometries.extend(create_helicon_pattern('xz', intersection_points_3d))

    # Visualization
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="3D Helicon Geometry with Intersections")

    for geometry in geometries:
        vis.add_geometry(geometry)

    # Set default camera view
    ctr = vis.get_view_control()
    ctr.set_zoom(0.8)
    ctr.set_front([-0.5, -0.5, -0.5])
    ctr.set_up([0, 0, 1])

    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    visualize_3d_helicon()