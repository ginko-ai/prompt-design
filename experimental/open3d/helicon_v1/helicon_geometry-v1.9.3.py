# add updated target diagram highlighting intersection points
import open3d as o3d
import numpy as np
from math import pi, cos, sin, sqrt


# [Previous helper functions remain the same]
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

def calculate_intersection_points():
    # Basic structure points (yellow dots)
    points = [
        # Square corners
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        # Edge midpoints
        [0, -1, 0], [1, 0, 0], [0, 1, 0], [-1, 0, 0],
        # Quarter points on each edge
        [-0.5, -1, 0], [0.5, -1, 0],
        [1, -0.5, 0], [1, 0.5, 0],
        [0.5, 1, 0], [-0.5, 1, 0],
        [-1, 0.5, 0], [-1, -0.5, 0],
        # Grid intersection points
        [-0.5, 0, 0], [0.5, 0, 0],
        [0, -0.5, 0], [0, 0.5, 0],
    ]
    return np.array(points)

def calculate_triangle_special_intersections():
    # Black dots - intersections with triangle edges
    points = [
        # With semi-circles
        [-0.866, -0.5, 0],  # Left side with bottom semi-circle
        [0.866, -0.5, 0],   # Right side with bottom semi-circle
        [-0.5, 0.3, 0],     # Left side with left semi-circle
        [0.5, 0.3, 0],      # Right side with right semi-circle

        # With diagonals
        [-0.5, -0.5, 0],    # Left side with diagonal
        [0.5, -0.5, 0],     # Right side with diagonal

        # With bisection lines
        [0, 0, 0],          # Center point
        [-0.333, 0, 0],     # Left side with vertical bisector
        [0.333, 0, 0],      # Right side with vertical bisector
    ]
    return np.array(points)

def create_helicon_geometry():
    geometries = []

    # [Previous geometry creation remains similar]
    # Base square
    square_points = np.array([[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0], [-1, -1, 0]])
    square_lines = o3d.geometry.LineSet()
    square_lines.points = o3d.utility.Vector3dVector(square_points)
    square_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(4)])
    square_lines.paint_uniform_color([0.8, 0.8, 0.8])
    geometries.append(square_lines)

    # Single isosceles triangle
    triangle_points = np.array([
        [-1, -1, 0],  # Left base point
        [1, -1, 0],   # Right base point
        [0, 1, 0]     # Apex
    ])
    triangle_lines = o3d.geometry.LineSet()
    triangle_lines.points = o3d.utility.Vector3dVector(triangle_points)
    triangle_lines.lines = o3d.utility.Vector2iVector([
        [0, 1],  # Base
        [1, 2],  # Right side
        [2, 0]   # Left side
    ])
    triangle_lines.paint_uniform_color([0.4, 0.4, 0.8])
    geometries.append(triangle_lines)

    # Main circle
    circle_points = create_circle_points([0, 0], 1)
    circle_lines = o3d.geometry.LineSet()
    circle_lines.points = o3d.utility.Vector3dVector(circle_points)
    circle_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(len(circle_points)-1)])
    circle_lines.paint_uniform_color([0.2, 0.8, 0.2])
    geometries.append(circle_lines)

    # Semi-circles
    semicircle_centers = [
        ([0, -1], 0),    # Bottom
        ([1, 0], pi/2),  # Right
        ([0, 1], pi),    # Top
        ([-1, 0], -pi/2) # Left
    ]

    for center, start_angle in semicircle_centers:
        semi_points = create_semicircle_points(center, 1, start_angle)
        semi_lines = o3d.geometry.LineSet()
        semi_lines.points = o3d.utility.Vector3dVector(semi_points)
        semi_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(len(semi_points)-1)])
        semi_lines.paint_uniform_color([0.8, 0.4, 0.4])
        geometries.append(semi_lines)

    # Diagonal lines
    diagonal_points = [
        [[-1, -1, 0], [1, 1, 0]],
        [[1, -1, 0], [-1, 1, 0]]
    ]
    for points in diagonal_points:
        diag_lines = o3d.geometry.LineSet()
        diag_lines.points = o3d.utility.Vector3dVector(points)
        diag_lines.lines = o3d.utility.Vector2iVector([[0, 1]])
        diag_lines.paint_uniform_color([0.4, 0.4, 0.8])
        geometries.append(diag_lines)

    # Regular intersection points (yellow)
    for point in calculate_intersection_points():
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
        sphere.translate(point)
        sphere.paint_uniform_color([1.0, 0.8, 0.0])
        geometries.append(sphere)

    # Triangle special intersection points (black with white outline)
    for point in calculate_triangle_special_intersections():
        # Black inner sphere
        sphere_inner = o3d.geometry.TriangleMesh.create_sphere(radius=0.025)
        sphere_inner.translate(point)
        sphere_inner.paint_uniform_color([0.0, 0.0, 0.0])
        geometries.append(sphere_inner)

        # White outer sphere (slightly larger)
        sphere_outer = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
        sphere_outer.translate(point)
        sphere_outer.paint_uniform_color([1.0, 1.0, 1.0])
        geometries.append(sphere_outer)

    # Harmonic ratio lines
    ratios = [0.5, 1/3, 0.25, 0.2]
    for ratio in ratios:
        points = np.array([
            [ratio * 2 - 1, -1, 0],
            [ratio * 2 - 1, 1, 0]
        ])
        ratio_line = o3d.geometry.LineSet()
        ratio_line.points = o3d.utility.Vector3dVector(points)
        ratio_line.lines = o3d.utility.Vector2iVector([[0, 1]])
        ratio_line.paint_uniform_color([0.8, 0.6, 0.4])
        geometries.append(ratio_line)

    return geometries

def visualize_helicon():
    geometries = create_helicon_geometry()

    # Create coordinate frame
    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=0.5, origin=[0, 0, 0])
    geometries.append(coord_frame)

    # Visualization settings
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Helicon Geometry with Special Intersections")

    for geometry in geometries:
        vis.add_geometry(geometry)

    # Set default camera view
    ctr = vis.get_view_control()
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, 0, 1])
    ctr.set_front([0, -1, 0.5])
    ctr.set_zoom(0.7)

    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    visualize_helicon()
