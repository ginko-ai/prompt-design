# 2nd attempt at removing larger octagon and highlighting inner octagon
import open3d as o3d
import numpy as np
from math import pi, cos, sin

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

def create_helicon_geometry():
    geometries = []

    # Harmonic ratios
    ratios = [0.5, 1/3, 0.25, 0.2]  # 1/2, 1/3, 1/4, 1/5

    # Base square vertices
    square_points = np.array([
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        [-1, -1, 0]
    ])

    # Square lines
    square_lines = o3d.geometry.LineSet()
    square_lines.points = o3d.utility.Vector3dVector(square_points)
    square_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(4)])
    square_lines.paint_uniform_color([0.8, 0.8, 0.8])
    geometries.append(square_lines)

    # Circle within square
    circle_points = create_circle_points([0, 0], 1)
    circle_lines = o3d.geometry.LineSet()
    circle_lines.points = o3d.utility.Vector3dVector(circle_points)
    circle_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(len(circle_points)-1)])
    circle_lines.paint_uniform_color([0.2, 0.8, 0.2])
    geometries.append(circle_lines)

    # Four semi-circles
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

    # Inner octagon points based on harmonic ratios
    r1, r2, r3, r4 = ratios[0], ratios[1], ratios[2], ratios[3]
    inner_octagon_points = np.array([
        [-r1, -r3, 0], [r1, -r3, 0],  # Bottom points using 1/2 and 1/4
        [r3, -r1, 0], [r3, r1, 0],    # Right points using 1/4 and 1/2
        [r1, r3, 0], [-r1, r3, 0],    # Top points using 1/2 and 1/4
        [-r3, r1, 0], [-r3, -r1, 0],  # Left points using 1/4 and 1/2
        [-r1, -r3, 0]                  # Close the loop
    ])

    # Inner octagon lines (highlighted)
    inner_octagon_lines = o3d.geometry.LineSet()
    inner_octagon_lines.points = o3d.utility.Vector3dVector(inner_octagon_points)
    inner_octagon_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(8)])
    inner_octagon_lines.paint_uniform_color([1.0, 0.6, 0.0])  # Bright orange for emphasis
    geometries.append(inner_octagon_lines)

    # Four isosceles triangles aligned with harmonic ratios
    triangle_points = [
        # Bottom-based triangle
        [[-1, -1, 0], [1, -1, 0], [0, r2, 0]],  # Peak at 1/3 ratio
        # Right-based triangle
        [[1, -1, 0], [1, 1, 0], [-r2, 0, 0]],   # Peak at 1/3 ratio
        # Top-based triangle
        [[1, 1, 0], [-1, 1, 0], [0, -r2, 0]],   # Peak at 1/3 ratio
        # Left-based triangle
        [[-1, 1, 0], [-1, -1, 0], [r2, 0, 0]]   # Peak at 1/3 ratio
    ]

    for triangle in triangle_points:
        tri_lines = o3d.geometry.LineSet()
        points = np.array(triangle + [triangle[0]])  # Close the triangle
        tri_lines.points = o3d.utility.Vector3dVector(points)
        tri_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(3)])
        tri_lines.paint_uniform_color([0.4, 0.4, 0.8])
        geometries.append(tri_lines)

    # Harmonic ratio lines
    for ratio in ratios:
        points = np.array([
            [ratio * 2 - 1, -1, 0],
            [ratio * 2 - 1, 1, 0]
        ])
        ratio_line = o3d.geometry.LineSet()
        ratio_line.points = o3d.utility.Vector3dVector(points)
        ratio_line.lines = o3d.utility.Vector2iVector([[0, 1]])
        ratio_line.paint_uniform_color([1.0, 0.6, 0.6])
        geometries.append(ratio_line)

    # Intersection points
    intersection_points = [
        # Square corners
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        # Harmonic ratio points on vertical lines
        [-r1, 0, 0], [r1, 0, 0],  # 1/2
        [-r2, 0, 0], [r2, 0, 0],  # 1/3
        [-r3, 0, 0], [r3, 0, 0],  # 1/4
        [-r4, 0, 0], [r4, 0, 0],  # 1/5
        # Inner octagon vertices (all 8 points)
        *inner_octagon_points[:-1],
        # Center point
        [0, 0, 0]
    ]

    for point in intersection_points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
        sphere.translate(point)
        sphere.paint_uniform_color([1.0, 0.8, 0.0])
        geometries.append(sphere)

    return geometries

def visualize_helicon():
    geometries = create_helicon_geometry()

    # Create coordinate frame
    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=0.5, origin=[0, 0, 0])
    geometries.append(coord_frame)

    # Visualization settings
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Refined Helicon Geometry")

    for geometry in geometries:
        vis.add_geometry(geometry)

    # Set default camera view
    ctr = vis.get_view_control()
    ctr.set_lookat([0, 0, 0])
    ctr.set_up([0, 0, 1])
    ctr.set_front([0, -1, 0.5])
    ctr.set_zoom(0.7)

    # Run visualization
    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    visualize_helicon()