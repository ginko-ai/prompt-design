# another attempt
import open3d as o3d
import numpy as np
from math import pi, cos, sin, sqrt

# [Previous helper functions remain the same]

def calculate_triangle_intersections():
    # Dictionary to store points with their IDs
    intersection_points = {
        # Triangle-Semicircle intersections
        'TS1': [-0.866, -0.5, 0],   # Left side with bottom semicircle
        'TS2': [0.866, -0.5, 0],    # Right side with bottom semicircle
        'TS3': [-0.5, 0.5, 0],      # Left side with left semicircle
        'TS4': [0.5, 0.5, 0],       # Right side with right semicircle

        # Triangle-Diagonal intersections
        'TD1': [-0.5, -0.5, 0],     # Left side with diagonal
        'TD2': [0.5, -0.5, 0],      # Right side with diagonal
        'TD3': [0, 0.333, 0],       # Center intersection point

        # Triangle-Bisection intersections
        'TB1': [0, -0.5, 0],        # With vertical bisection
        'TB2': [-0.5, 0, 0],        # Left side with horizontal bisection
        'TB3': [0.5, 0, 0],         # Right side with horizontal bisection
    }
    return intersection_points

def create_helicon_geometry():
    geometries = []

    # [Previous geometry creation remains similar]

    # Add black intersection points with IDs
    intersection_points = calculate_triangle_intersections()
    for point_id, point in intersection_points.items():
        # Create black sphere for intersection
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.025)
        sphere.translate(point)
        sphere.paint_uniform_color([0.0, 0.0, 0.0])  # Black color
        geometries.append(sphere)

        # Add text label for debugging (commenting out for now as Open3D doesn't support text directly)
        # You might want to print these coordinates for debugging
        print(f"Intersection {point_id}: {point}")

    # [Rest of the geometry creation remains the same]

    return geometries

def visualize_helicon():
    geometries = create_helicon_geometry()

    # Create coordinate frame
    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=0.5, origin=[0, 0, 0])
    geometries.append(coord_frame)

    # Visualization settings
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Helicon Geometry with Triangle Intersections")

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
    