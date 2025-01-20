import open3d as o3d
import numpy as np
from math import pi, cos, sin, sqrt

def create_helicon_geometry():
    geometries = []

    # Base square vertices (keeping original)
    square_points = np.array([
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        [-1, -1, 0]
    ])
    square_lines = o3d.geometry.LineSet()
    square_lines.points = o3d.utility.Vector3dVector(square_points)
    square_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(4)])
    square_lines.paint_uniform_color([0.8, 0.8, 0.8])
    geometries.append(square_lines)

    # 1. Circle within square
    circle_points = []
    num_segments = 100
    for i in range(num_segments + 1):
        angle = 2 * pi * i / num_segments
        circle_points.append([cos(angle), sin(angle), 0])

    circle_lines = o3d.geometry.LineSet()
    circle_lines.points = o3d.utility.Vector3dVector(circle_points)
    circle_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(num_segments)])
    circle_lines.paint_uniform_color([0.0, 0.8, 0.0])
    geometries.append(circle_lines)

    # 2. Four semi-circles
    def create_semicircle(center, radius, start_angle):
        points = []
        segments = 50
        for i in range(segments + 1):
            angle = start_angle + pi * i / segments
            points.append([
                center[0] + radius * cos(angle),
                center[1] + radius * sin(angle),
                0
            ])
        return points

    semicircle_colors = [[0.8, 0.4, 0.4], [0.4, 0.8, 0.4],
                        [0.4, 0.4, 0.8], [0.8, 0.8, 0.4]]

    # Bottom, Right, Top, Left semicircles
    semicircle_params = [
        ([0, -1], 1, 0),    # Bottom
        ([1, 0], 1, pi/2),  # Right
        ([0, 1], 1, pi),    # Top
        ([-1, 0], 1, -pi/2) # Left
    ]

    for (center, radius, angle), color in zip(semicircle_params, semicircle_colors):
        points = create_semicircle(center, radius, angle)
        semi_lines = o3d.geometry.LineSet()
        semi_lines.points = o3d.utility.Vector3dVector(points)
        semi_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(len(points)-1)])
        semi_lines.paint_uniform_color(color)
        geometries.append(semi_lines)

    # 3. Four equilateral triangles
    triangle_height = sqrt(3)
    triangle_sets = [
        # Bottom triangle
        [[-1, -1, 0], [1, -1, 0], [0, -1 + triangle_height, 0]],
        # Right triangle
        [[1, -1, 0], [1, 1, 0], [1 - triangle_height, 0, 0]],
        # Top triangle
        [[1, 1, 0], [-1, 1, 0], [0, 1 - triangle_height, 0]],
        # Left triangle
        [[-1, 1, 0], [-1, -1, 0], [-1 + triangle_height, 0, 0]]
    ]

    for triangle_points in triangle_sets:
        triangle = o3d.geometry.LineSet()
        points = np.array(triangle_points + [triangle_points[0]])  # Close the triangle
        triangle.points = o3d.utility.Vector3dVector(points)
        triangle.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(3)])
        triangle.paint_uniform_color([0.8, 0.6, 0.0])
        geometries.append(triangle)

    # 4. Intersection points
    # Calculate key intersection points
    intersection_points = [
        # Square corners
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        # Circle-Square intersections
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0],
        # Triangle centers
        [0, -1 + triangle_height/3, 0],
        [1 - triangle_height/3, 0, 0],
        [0, 1 - triangle_height/3, 0],
        [-1 + triangle_height/3, 0, 0],
        # Center point
        [0, 0, 0]
    ]

    for point in intersection_points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.03)
        sphere.translate(point)
        sphere.paint_uniform_color([1.0, 0.0, 0.0])
        geometries.append(sphere)

    # Add original Helicon elements (keeping from previous version)
    # Octagon
    octagon_points = np.array([
        [-1, -0.414, 0], [-0.414, -1, 0], [0.414, -1, 0], [1, -0.414, 0],
        [1, 0.414, 0], [0.414, 1, 0], [-0.414, 1, 0], [-1, 0.414, 0],
        [-1, -0.414, 0]
    ])
    octagon_lines = o3d.geometry.LineSet()
    octagon_lines.points = o3d.utility.Vector3dVector(octagon_points)
    octagon_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(8)])
    octagon_lines.paint_uniform_color([0.6, 0.6, 1.0])
    geometries.append(octagon_lines)

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