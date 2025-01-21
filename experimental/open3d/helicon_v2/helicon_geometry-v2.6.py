# verify context carrys over to new chat
import open3d as o3d
import numpy as np
from math import pi, cos, sin, sqrt

def create_cube_edges():
    points = np.array([
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ])
    lines = [[0, 1], [1, 2], [2, 3], [3, 0],
             [4, 5], [5, 6], [6, 7], [7, 4],
             [0, 4], [1, 5], [2, 6], [3, 7]]

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.paint_uniform_color([0.5, 0.5, 0.5])
    return line_set

def create_pattern_in_plane(plane='xy'):
    geometries = []
    scale = 1.0

    if plane == 'xy':
        z = -1
        transform = np.eye(4)
    elif plane == 'yz':
        z = -1
        transform = np.array([
            [0, -1, 0, 0],
            [0, 0, -1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1]
        ])
    elif plane == 'xz':
        z = 1
        transform = np.array([
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])

    # Create circle
    circle_points = []
    for i in range(51):
        theta = 2 * pi * i / 50
        x = scale * cos(theta)
        y = scale * sin(theta)
        circle_points.append([x, y, z])

    circle_lines = o3d.geometry.LineSet()
    circle_lines.points = o3d.utility.Vector3dVector(circle_points)
    circle_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(50)])
    circle_lines.paint_uniform_color([0, 0, 1])

    # Transform and add geometries
    circle_lines.transform(transform)
    geometries.append(circle_lines)

    # Add intersection points
    intersection_points = [
        # Central axis points
        [0, 0.5, z], [0, -0.5, z], [0.5, 0, z], [-0.5, 0, z],
        # Left/Right clusters
        [0.6, 0.2, z], [0.6, -0.2, z], [-0.6, 0.2, z], [-0.6, -0.2, z],
        [0.333, 0.333, z], [0.333, -0.333, z], [-0.333, 0.333, z], [-0.333, -0.333, z],
        [0.2, 0.6, z], [0.2, -0.6, z], [-0.2, 0.6, z], [-0.2, -0.6, z]
    ]

    for point in intersection_points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
        sphere.translate(point)
        sphere.transform(transform)
        sphere.paint_uniform_color([0.5, 1.0, 0.5])  # Light green
        geometries.append(sphere)

    return geometries

def find_triple_intersections(tolerance=0.01):
    # Define reference points for each plane
    xy_points = np.array([
        [0, 0.5, -1], [0, -0.5, -1], [0.5, 0, -1], [-0.5, 0, -1],
        [0.6, 0.2, -1], [0.6, -0.2, -1], [-0.6, 0.2, -1], [-0.6, -0.2, -1],
        [0.333, 0.333, -1], [0.333, -0.333, -1], [-0.333, 0.333, -1], [-0.333, -0.333, -1],
        [0.2, 0.6, -1], [0.2, -0.6, -1], [-0.2, 0.6, -1], [-0.2, -0.6, -1]
    ])

    triple_points = []

    # Project points and find intersections
    for point in xy_points:
        # Project point through cube
        projection = np.array([
            [point[0], point[1], z] for z in np.linspace(-1, 1, 100)
        ])

        # Check for intersections with other planes' points
        for proj_point in projection:
            if (np.abs(proj_point) <= 1).all():  # Inside cube bounds
                triple_points.append(proj_point)

    return np.array(triple_points)

def visualize_3d_helicon():
    # Create visualization window
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="3D Helicon Geometry")

    # Add cube edges
    cube = create_cube_edges()
    vis.add_geometry(cube)

    # Add patterns in each plane
    for plane in ['xy', 'yz', 'xz']:
        geometries = create_pattern_in_plane(plane)
        for geom in geometries:
            vis.add_geometry(geom)

    # Add triple intersections
    triple_points = find_triple_intersections()
    for point in triple_points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
        sphere.translate(point)
        sphere.paint_uniform_color([0.8, 0.3, 0.8])  # Purple
        vis.add_geometry(sphere)

    # Set default camera view
    ctr = vis.get_view_control()
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, 0, 1])
    ctr.set_front([-0.5, -0.5, -0.5])
    ctr.set_zoom(0.8)

    # Run visualization
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    visualize_3d_helicon()