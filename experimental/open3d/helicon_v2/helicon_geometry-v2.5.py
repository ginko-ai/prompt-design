# 2nd attempt
import open3d as o3d
import numpy as np
from math import pi, cos, sin
from itertools import combinations

def find_triple_intersections(points_xy, points_yz, points_xz):
    """
    Find points where projections from all three faces intersect.
    Returns list of intersection points and their source points.
    """
    triple_intersections = []
    tolerance = 0.01  # Intersection tolerance

    for px in points_xy:
        for py in points_yz:
            for pz in points_xz:
                # Project lines from each face
                x_coord = px[0]  # From xy-plane
                y_coord = py[1]  # From yz-plane
                z_coord = pz[2]  # From xz-plane

                # Check if the lines would intersect (within tolerance)
                if (abs(px[1] - y_coord) < tolerance and
                    abs(py[2] - z_coord) < tolerance and
                    abs(pz[0] - x_coord) < tolerance):

                    intersection = np.array([x_coord, y_coord, z_coord])
                    # Check if point is inside cube
                    if all(abs(intersection) <= 1):
                        triple_intersections.append({
                            'point': intersection,
                            'sources': (px, py, pz)
                        })

    return triple_intersections

def create_cube_faces():
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

def transform_intersection_points(points, plane='xy'):
    """Transform points based on which face they're on"""
    points_array = np.array(points)
    transformed_points = []

    if plane == 'xy':
        transformed_points = np.column_stack([points_array[:, 0], points_array[:, 1], np.ones(len(points_array))])
    elif plane == 'yz':
        transformed_points = np.column_stack([np.ones(len(points_array)), points_array[:, 0], points_array[:, 1]])
    elif plane == 'xz':
        transformed_points = np.column_stack([points_array[:, 0], np.ones(len(points_array)), points_array[:, 1]])

    return transformed_points

def create_helicon_pattern(plane='xy', triple_intersections=None):
    geometries = []

    # Transform matrices for different faces
    if plane == 'xy':
        transform = np.eye(4)
        transform[2, 3] = 1
    elif plane == 'yz':
        transform = np.array([
            [0, 0, -1, 1],
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1]
        ])
    elif plane == 'xz':
        transform = np.array([
            [1, 0, 0, 0],
            [0, 0, -1, 1],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])

    # Original intersection points scaled to unit cube
    base_points = np.array([
        # Central axis points
        [0, 0.5, 0], [0, -0.5, 0], [0.5, 0, 0], [-0.5, 0, 0],
        # Left side clusters
        [-0.6, 0.2, 0], [-0.6, -0.2, 0], [-0.333, 0.333, 0], [-0.333, -0.333, 0],
        [-0.2, 0.6, 0], [-0.2, -0.6, 0],
        # Right side clusters
        [0.6, 0.2, 0], [0.6, -0.2, 0], [0.333, 0.333, 0], [0.333, -0.333, 0],
        [0.2, 0.6, 0], [0.2, -0.6, 0]
    ])

    # Transform points based on which face they're on
    points = transform_intersection_points(base_points, plane)

    # Create projection lines and points
    for point in points:
        # Convert point to numpy array if it isn't already
        point = np.array(point)

        # Create intersection point sphere
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
        sphere.translate(point)

        # Color based on whether this point participates in a triple intersection
        if triple_intersections and any(np.allclose(point, src) for intr in triple_intersections for src in intr['sources']):
            sphere.paint_uniform_color([0.8, 0.4, 0.8])  # Purple for triple intersection sources
        else:
            sphere.paint_uniform_color([0.5, 1, 0.5])  # Light green for regular points

        geometries.append(sphere)

        # Create projection line with numpy arrays
        if plane == 'xy':
            end_point = point - np.array([0, 0, 2])
        elif plane == 'yz':
            end_point = point - np.array([2, 0, 0])
        else:  # xz
            end_point = point - np.array([0, 2, 0])

        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector([point, end_point])
        line.lines = o3d.utility.Vector2iVector([[0, 1]])
        line.paint_uniform_color([0.8, 0.8, 0.8])
        geometries.append(line)

    return geometries, points

def visualize_3d_helicon():
    geometries = []

    # Add cube faces
    geometries.append(create_cube_faces())

    # Generate patterns and collect points from each face
    xy_geometries, xy_points = create_helicon_pattern('xy')
    yz_geometries, yz_points = create_helicon_pattern('yz')
    xz_geometries, xz_points = create_helicon_pattern('xz')

    # Find triple intersections
    triple_intersections = find_triple_intersections(xy_points, yz_points, xz_points)

    # Regenerate patterns with triple intersection information
    xy_geometries, _ = create_helicon_pattern('xy', triple_intersections=triple_intersections)
    yz_geometries, _ = create_helicon_pattern('yz', triple_intersections=triple_intersections)
    xz_geometries, _ = create_helicon_pattern('xz', triple_intersections=triple_intersections)

    geometries.extend(xy_geometries)
    geometries.extend(yz_geometries)
    geometries.extend(xz_geometries)

    # Add triple intersection points
    for intersection in triple_intersections:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
        sphere.translate(intersection['point'])
        sphere.paint_uniform_color([0.8, 0.2, 0.8])  # Bright purple
        geometries.append(sphere)

        # Print intersection coordinates for verification
        print(f"Triple intersection found at: {intersection['point']}")

    # Visualization
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="3D Helicon Geometry with Triple Intersections")

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