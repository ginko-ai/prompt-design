# add intersection ids

"""
@startuml
title classDiagram
    class HeliconGeometry {
        -geometries: list
        +create_helicon_geometry()
        +visualize_helicon()
    }

    class GeometryCreator {
        +create_circle_points(center, radius, num_points)
        +create_semicircle_points(center, radius, start_angle, num_points)
        +create_intersection_sphere(point, intersection_type)
    }

    class IntersectionCalculator {
        +calculate_intersection_points()
        +calculate_triangle_semicircle_intersections()
    }

    class Primitives {
        -square_points: np.array
        -triangle_points: np.array
        -circle_points: np.array
        -semicircle_points: np.array
        -diagonal_points: np.array
        +create_square()
        +create_triangle()
        +create_circle()
        +create_semicircles()
        +create_diagonals()
    }

    class Visualizer {
        -vis: o3d.visualization.Visualizer
        +create_window(title)
        +set_camera_view()
        +add_geometries(geometries)
        +run()
        +destroy_window()
    }

    class GeometryTypes {
        <<enumeration>>
        SEMICIRCLE
        DIAGONAL
        BISECTION
    }

    class Point3D {
        +x: float
        +y: float
        +z: float
        +type: string
        +id: int
    }

    class LineSet {
        +points: Vector3dVector
        +lines: Vector2iVector
        +color: array
    }

    HeliconGeometry --> GeometryCreator : uses
    HeliconGeometry --> IntersectionCalculator : uses
    HeliconGeometry --> Primitives : uses
    HeliconGeometry --> Visualizer : uses
    GeometryCreator ..> Point3D : creates
    GeometryCreator ..> LineSet : creates
    Primitives ..> LineSet : creates
    IntersectionCalculator ..> Point3D : creates
    IntersectionCalculator ..> GeometryTypes : uses
    Visualizer --> LineSet : renders
@enduml
"""




import open3d as o3d
import numpy as np
from math import pi, cos, sin, sqrt

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
    points = [
        # Center
        [0, 0, 0],
        # Square corners
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        # Edge midpoints
        [0, -1, 0], [1, 0, 0], [0, 1, 0], [-1, 0, 0],
        # Quarter points on each edge
        [-0.5, -1, 0], [0.5, -1, 0],
        [1, -0.5, 0], [1, 0.5, 0],
        [0.5, 1, 0], [-0.5, 1, 0],
        [-1, 0.5, 0], [-1, -0.5, 0],
        # Inner ring points
        [-0.5, 0, 0], [0.5, 0, 0],
        [0, -0.5, 0], [0, 0.5, 0],
        # Diagonal intersection points
        [-0.707, -0.707, 0], [0.707, -0.707, 0],
        [0.707, 0.707, 0], [-0.707, 0.707, 0]
    ]
    return np.array(points)

def calculate_triangle_semicircle_intersections():
    intersections = [
        # Format: [x, y, z, intersection_type, id]
        # Left side intersections with semicircles
        [-0.866, -0.5, 0, "semicircle", 1],  # Bottom semicircle
        [-0.5, 0, 0, "semicircle", 2],       # Left semicircle
        [-0.5, 0.5, 0, "semicircle", 3],     # Left semicircle

        # Right side intersections with semicircles
        [0.866, -0.5, 0, "semicircle", 4],   # Bottom semicircle
        [0.5, 0, 0, "semicircle", 5],        # Right semicircle
        [0.5, 0.5, 0, "semicircle", 6],      # Right semicircle

        # Intersections with diagonals
        [-0.707, -0.707, 0, "diagonal", 7],  # Left diagonal
        [0.707, -0.707, 0, "diagonal", 8],   # Right diagonal
        [-0.5, 0.5, 0, "diagonal", 9],       # Left upper diagonal
        [0.5, 0.5, 0, "diagonal", 10],       # Right upper diagonal

        # Intersections with bisections
        [0, -0.5, 0, "bisection", 11],       # Bottom bisection
        [-0.5, 0, 0, "bisection", 12],       # Left bisection
        [0.5, 0, 0, "bisection", 13],        # Right bisection
        [0, 0.5, 0, "bisection", 14],        # Top bisection
    ]
    return np.array(intersections)

def create_intersection_sphere(point, intersection_type):
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
    sphere.translate(point[:3])  # Only use x, y, z coordinates

    # Color based on intersection type
    if intersection_type == "semicircle":
        sphere.paint_uniform_color([0, 0, 0])  # Black
    elif intersection_type == "diagonal":
        sphere.paint_uniform_color([0, 0, 0])  # Black
    elif intersection_type == "bisection":
        sphere.paint_uniform_color([0, 0, 0])  # Black
    else:
        sphere.paint_uniform_color([1.0, 0.8, 0.0])  # Default yellow

    return sphere

def create_helicon_geometry():
    geometries = []

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

    # Grid lines
    grid_points = calculate_intersection_points()
    for i in range(len(grid_points)):
        for j in range(i+1, len(grid_points)):
            if abs(grid_points[i][0] - grid_points[j][0]) < 1e-6 or \
               abs(grid_points[i][1] - grid_points[j][1]) < 1e-6:
                grid_line = o3d.geometry.LineSet()
                line_points = np.array([grid_points[i], grid_points[j]])
                grid_line.points = o3d.utility.Vector3dVector(line_points)
                grid_line.lines = o3d.utility.Vector2iVector([[0, 1]])
                grid_line.paint_uniform_color([1.0, 0.8, 0.0])
                geometries.append(grid_line)

    # Regular intersection points (yellow)
    for point in calculate_intersection_points():
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.02)
        sphere.translate(point)
        sphere.paint_uniform_color([1.0, 0.8, 0.0])
        geometries.append(sphere)

    # Triangle intersection points (black)
    intersection_data = calculate_triangle_semicircle_intersections()
    for point in intersection_data:
        intersection_type = point[3]
        sphere = create_intersection_sphere(point, intersection_type)
        geometries.append(sphere)

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
    vis.create_window(window_name="Helicon Geometry with Triangle-Semicircle Intersections")

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