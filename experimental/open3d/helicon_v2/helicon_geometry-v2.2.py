# add helicon diagram to 6 faces of a cube
import open3d as o3d
import numpy as np
from math import pi, cos, sin
from copy import deepcopy

def create_circle_points(center, radius, num_points=50):
    points = []
    for i in range(num_points + 1):
        theta = 2 * pi * i / num_points
        x = center[0] + radius * cos(theta)
        y = center[1] + radius * sin(theta)
        points.append([x, y, 0])
    return np.array(points)

def create_semicircle_points(center, radius, start_angle, num_points=25):
    points = []
    for i in range(num_points + 1):
        theta = start_angle + pi * i / num_points
        x = center[0] + radius * cos(theta)
        y = center[1] + radius * sin(theta)
        points.append([x, y, 0])
    return np.array(points)

def create_sphere_marker(point, color):
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.3)
    sphere.translate(point)
    sphere.paint_uniform_color(color)
    return sphere

def create_single_face_geometry():
    geometries = []
    scale = 10  # Scale factor to match the -10 to 10 coordinate system

    # Base circle (blue)
    circle_points = create_circle_points([0, 0], scale)
    circle_lines = o3d.geometry.LineSet()
    circle_lines.points = o3d.utility.Vector3dVector(circle_points)
    circle_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(len(circle_points)-1)])
    circle_lines.paint_uniform_color([0, 0, 1])  # Blue
    geometries.append(circle_lines)

    # Square and diagonals (green)
    square_points = np.array([
        [-scale, -scale, 0], [scale, -scale, 0],
        [scale, scale, 0], [-scale, scale, 0],
        [-scale, -scale, 0]
    ])
    square_lines = o3d.geometry.LineSet()
    square_lines.points = o3d.utility.Vector3dVector(square_points)
    square_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(4)])
    square_lines.paint_uniform_color([0, 1, 0])  # Green
    geometries.append(square_lines)

    # Diagonals (green)
    diagonal_points = np.array([
        [-scale, -scale, 0], [scale, scale, 0],
        [scale, -scale, 0], [-scale, scale, 0]
    ])
    diagonal_lines = o3d.geometry.LineSet()
    diagonal_lines.points = o3d.utility.Vector3dVector(diagonal_points)
    diagonal_lines.lines = o3d.utility.Vector2iVector([[0, 1], [2, 3]])
    diagonal_lines.paint_uniform_color([0, 1, 0])  # Green
    geometries.append(diagonal_lines)

    # Semi-circles (light blue)
    semicircle_centers = [
        ([scale, 0], pi/2),    # Right
        ([-scale, 0], -pi/2),  # Left
        ([0, scale], pi),      # Top
        ([0, -scale], 0)       # Bottom
    ]

    for center, start_angle in semicircle_centers:
        semi_points = create_semicircle_points(center, scale, start_angle)
        semi_lines = o3d.geometry.LineSet()
        semi_lines.points = o3d.utility.Vector3dVector(semi_points)
        semi_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(len(semi_points)-1)])
        semi_lines.paint_uniform_color([0.5, 0.8, 1])  # Light blue
        geometries.append(semi_lines)

    # Triangle lines (orange)
    triangle_points = [
        # T1
        [[-scale, scale, 0], [0, -scale, 0]],  # Line1
        [[scale, scale, 0], [0, -scale, 0]],   # Line2
        # T2
        [[-scale, -scale, 0], [scale, 0, 0]],  # Line4
        [[-scale, scale, 0], [scale, 0, 0]],   # Line5
        # T3
        [[scale, -scale, 0], [0, scale, 0]],   # Line7
        [[-scale, -scale, 0], [0, scale, 0]],  # Line8
        # T4
        [[scale, -scale, 0], [-scale, 0, 0]],  # Line10
        [[scale, scale, 0], [-scale, 0, 0]]    # Line11
    ]

    for points in triangle_points:
        line = o3d.geometry.LineSet()
        line.points = o3d.utility.Vector3dVector(points)
        line.lines = o3d.utility.Vector2iVector([[0, 1]])
        line.paint_uniform_color([1, 0.5, 0])  # Orange
        geometries.append(line)

    # Red markers (square corners and circle-square intersections)
    red_points = [
        [scale, scale, 0], [scale, -scale, 0],    # Right corners
        [-scale, scale, 0], [-scale, -scale, 0],  # Left corners
        [scale, 0, 0], [-scale, 0, 0],           # Side intersections
        [0, scale, 0], [0, -scale, 0]            # Top/bottom intersections
    ]

    for point in red_points:
        geometries.append(create_sphere_marker(point, [1, 0, 0]))  # Red

    # Purple markers (line intersections)
    purple_points = [
        [-5, 0, 0], [0, 0, 0], [5, 0, 0],  # Horizontal row
        [0, 5, 0], [0, -5, 0]              # Vertical column
    ]

    for point in purple_points:
        geometries.append(create_sphere_marker(point, [0.5, 0, 0.5]))  # Purple

    return geometries

def transform_geometries(geometries, rotation_matrix, translation):
    transformed_geometries = []
    for geometry in geometries:
        transformed = deepcopy(geometry)
        transformed.transform(np.vstack((np.hstack((rotation_matrix, translation.reshape(3, 1))),
                                      np.array([0, 0, 0, 1]))))
        transformed_geometries.append(transformed)
    return transformed_geometries

def create_cube_faces():
    scale = 10
    all_geometries = []

    # Front face (z = scale)
    front_geometries = create_single_face_geometry()
    front_rotation = np.eye(3)
    front_translation = np.array([0, 0, scale])
    all_geometries.extend(transform_geometries(front_geometries, front_rotation, front_translation))

    # Back face (z = -scale)
    back_rotation = np.array([
        [-1, 0, 0],
        [0, 1, 0],
        [0, 0, -1]
    ])
    back_translation = np.array([0, 0, -scale])
    all_geometries.extend(transform_geometries(front_geometries, back_rotation, back_translation))

    # Right face (x = scale)
    right_rotation = np.array([
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]
    ])
    right_translation = np.array([scale, 0, 0])
    all_geometries.extend(transform_geometries(front_geometries, right_rotation, right_translation))

    # Left face (x = -scale)
    left_rotation = np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ])
    left_translation = np.array([-scale, 0, 0])
    all_geometries.extend(transform_geometries(front_geometries, left_rotation, left_translation))

    # Top face (y = scale)
    top_rotation = np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ])
    top_translation = np.array([0, scale, 0])
    all_geometries.extend(transform_geometries(front_geometries, top_rotation, top_translation))

    # Bottom face (y = -scale)
    bottom_rotation = np.array([
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0]
    ])
    bottom_translation = np.array([0, -scale, 0])
    all_geometries.extend(transform_geometries(front_geometries, bottom_rotation, bottom_translation))

    # Add coordinate frame
    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=scale/2, origin=[0, 0, 0])
    all_geometries.append(coord_frame)

    return all_geometries

def visualize_helicon_cube():
    geometries = create_cube_faces()

    # Visualization settings
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Helicon Geometry Cube")

    for geometry in geometries:
        vis.add_geometry(geometry)

    # Set default camera view
    ctr = vis.get_view_control()
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, 1, 0])
    ctr.set_front([1, -1, 1])
    ctr.set_zoom(0.5)

    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    visualize_helicon_cube()