import open3d as o3d
import numpy as np

def create_helicon_geometry():
    # Create an empty geometry list
    geometries = []

    # Base square vertices
    square_points = np.array([
        [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0],
        [-1, -1, 0]  # Closing the loop
    ])

    # Create square lines
    square_lines = o3d.geometry.LineSet()
    square_lines.points = o3d.utility.Vector3dVector(square_points)
    square_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(4)])
    square_lines.paint_uniform_color([0.8, 0.8, 0.8])
    geometries.append(square_lines)

    # Create octagon vertices
    octagon_points = np.array([
        [-1, -0.414, 0], [-0.414, -1, 0], [0.414, -1, 0], [1, -0.414, 0],
        [1, 0.414, 0], [0.414, 1, 0], [-0.414, 1, 0], [-1, 0.414, 0],
        [-1, -0.414, 0]  # Closing the loop
    ])

    # Create octagon lines
    octagon_lines = o3d.geometry.LineSet()
    octagon_lines.points = o3d.utility.Vector3dVector(octagon_points)
    octagon_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(8)])
    octagon_lines.paint_uniform_color([0.6, 0.6, 1.0])
    geometries.append(octagon_lines)

    # Create harmonic ratio lines (vertical)
    ratios = [0.5, 1/3, 0.25, 0.2]  # 1/2, 1/3, 1/4, 1/5
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

    # Create star pattern
    star_points = np.array([
        [0, -1, 0], [1, 0, 0], [0, 1, 0], [-1, 0, 0],
        [0, -1, 0]  # Closing the loop
    ])

    star_lines = o3d.geometry.LineSet()
    star_lines.points = o3d.utility.Vector3dVector(star_points)
    star_lines.lines = o3d.utility.Vector2iVector([[i, i+1] for i in range(4)])
    star_lines.paint_uniform_color([1.0, 1.0, 0.6])
    geometries.append(star_lines)

    # Create center point
    center_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
    center_sphere.paint_uniform_color([1.0, 0.6, 1.0])
    geometries.append(center_sphere)

    return geometries

def visualize_helicon():
    # Create geometry
    geometries = create_helicon_geometry()

    # Create coordinate frame
    coord_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=0.5, origin=[0, 0, 0])
    geometries.append(coord_frame)

    # Visualization settings
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Helicon Geometry")

    # Add geometries
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