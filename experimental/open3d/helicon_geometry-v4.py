# Remove outer octagon, hightlight inner octagon
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

def create_helicon_geometry():
    geometries = []

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

    # Four isosceles triangles
    triangle_points = [
        # Bottom-based triangle
        [[-1, -1, 0], [1, -1, 0], [0, 1, 0]],
        # Right-based triangle
        [[1, -1, 0], [1, 1, 0], [-1, 0, 0]],
        # Top-based triangle
        [[1, 1, 0], [-1, 1, 0], [0, -1, 0]],
        # Left-based triangle
        [[-1, 1, 0], [-1, -1, 0], [1, 0, 0]]
    ]

    for triangle in triangle_points:
        tri_lines = o3d.geometry.LineSet()
        points = np.array(triangle + [triangle[0]])  # Close the triangle
        tri_lines.points = o3d.utility.Vector3dVector(points)
        tri_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(3)])
        tri_lines.paint_uniform_color([0.4, 0.4, 0.8])
        geometries.append(tri_lines)

    # Inner octagon points (based on triangle intersections)
    # Calculate based on square with side length 2 (from -1 to 1)
    inner_factor = 1/sqrt(2)  # This gives us the correct intersection points
    inner_octagon_points = np.array([
        [-inner_factor, -inner_factor, 0],  # Bottom left
        [inner_factor, -inner_factor, 0],   # Bottom right
        [inner_factor, -inner_factor, 0],   # Right bottom
        [inner_factor, inner_factor, 0],    # Right top
        [inner_factor, inner_factor, 0],    # Top right
        [-inner_factor, inner_factor, 0],   # Top left
        [-inner_factor, inner_factor, 0],   # Left top
        [-inner_factor, -inner_factor, 0],  # Left bottom
        [-inner_factor, -inner_factor, 0]   # Close the loop
    ])

    # Create inner octagon with thicker lines and bright color
    inner_octagon = o3d.geometry.LineSet()
    inner_octagon.points = o3d.utility.Vector3dVector(inner_octagon_points)
    inner_octagon.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(8)])
    inner_octagon.paint_uniform_color([1.0, 0.6, 0.0])  # Bright orange color
    geometries.append(inner_octagon)

    # Intersection points
    intersection_points = [
        # Square corners
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        # Midpoints of square sides
        [0, -1, 0], [1, 0, 0], [0, 1, 0], [-1, 0, 0],
        # Center point
        [0, 0, 0],
        # Inner octagon vertices (triangle intersections)
        [-inner_factor, -inner_factor, 0], [inner_factor, -inner_factor, 0],
        [inner_factor, inner_factor, 0], [-inner_factor, inner_factor, 0]
    ]

    for point in intersection_points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
        sphere.translate(point)
        sphere.paint_uniform_color([1.0, 0.8, 0.0])
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
        ratio_line.paint_uniform_color([1.0, 0.6, 0.6])
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
    vis.create_window(window_name="Extended Helicon Geometry")

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