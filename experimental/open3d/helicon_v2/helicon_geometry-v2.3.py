# diagram on 3 faces of cube, project intersectons inward
import open3d as o3d
import numpy as np
from math import pi, cos, sin

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

def create_helicon_pattern(plane='xy'):
    geometries = []

    # Transform matrices for different faces
    if plane == 'xy':  # Front face
        transform = np.eye(4)
        transform[2, 3] = 1  # Move to z=1
    elif plane == 'yz':  # Right face
        transform = np.array([
            [0, 0, -1, 1],
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1]
        ])
    elif plane == 'xz':  # Top face
        transform = np.array([
            [1, 0, 0, 0],
            [0, 0, -1, 1],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])

    # Base circle
    circle_points = []
    for i in range(50):
        theta = 2 * pi * i / 49
        circle_points.append([cos(theta), sin(theta), 0])
    circle_points = np.array(circle_points)

    circle = o3d.geometry.LineSet()
    circle.points = o3d.utility.Vector3dVector(circle_points)
    circle.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(49)])
    circle.transform(transform)
    circle.paint_uniform_color([0, 0, 1])  # Blue
    geometries.append(circle)

    # Square
    square_points = np.array([[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0], [-1, -1, 0]])
    square = o3d.geometry.LineSet()
    square.points = o3d.utility.Vector3dVector(square_points)
    square.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(4)])
    square.transform(transform)
    square.paint_uniform_color([0, 1, 0])  # Green
    geometries.append(square)

    # Green intersection points (original 2D locations)
    intersection_points = [
        # Central axis points
        [0, 5, 0], [0, -5, 0], [5, 0, 0], [-5, 0, 0],
        # Left side clusters
        [-6, 2, 0], [-6, -2, 0], [-3.33, 3.33, 0], [-3.33, -3.33, 0], [-2, 6, 0], [-2, -6, 0],
        # Right side clusters
        [6, 2, 0], [6, -2, 0], [3.33, 3.33, 0], [3.33, -3.33, 0], [2, 6, 0], [2, -6, 0]
    ]

    # Scale points to match unit cube
    intersection_points = np.array(intersection_points) / 10.0

    # Create spheres for intersection points
    for point in intersection_points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
        transformed_point = np.dot(transform, np.append(point, 1))[:3]
        sphere.translate(transformed_point)
        sphere.paint_uniform_color([0.5, 1, 0.5])  # Light green
        geometries.append(sphere)

        # Create projection lines into the cube
        if plane == 'xy':
            line_points = np.array([transformed_point, transformed_point - [0, 0, 2]])
        elif plane == 'yz':
            line_points = np.array([transformed_point, transformed_point - [2, 0, 0]])
        elif plane == 'xz':
            line_points = np.array([transformed_point, transformed_point - [0, 2, 0]])

        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector(line_points)
        line.lines = o3d.utility.Vector2iVector([[0, 1]])
        line.paint_uniform_color([0.8, 0.8, 0.8])  # Light gray
        geometries.append(line)

    return geometries

def visualize_3d_helicon():
    geometries = []

    # Add cube faces
    geometries.append(create_cube_faces())

    # Add Helicon pattern to three faces
    geometries.extend(create_helicon_pattern('xy'))  # Front face
    geometries.extend(create_helicon_pattern('yz'))  # Right face
    geometries.extend(create_helicon_pattern('xz'))  # Top face

    # Visualization
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="3D Helicon Geometry")

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